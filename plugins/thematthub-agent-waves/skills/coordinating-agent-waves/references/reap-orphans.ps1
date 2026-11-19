# Find (and with -Stop -RepoRoot, end) leftover worker processes from agent runs.
# A process is a leftover when its parent process is gone and it is older than -MinAgeMinutes,
# or when its command line points into a worktree folder that no longer exists.
# Default is a dry run: it only lists. Processes whose parent is alive (an MCP server under
# claude.exe, a live pytest run) are never touched.
#
# Safety: a parentless python/node/browser process may belong to something else on the machine
# (a detached dev server, a notebook kernel). So -Stop is narrow:
#   - -Stop needs -RepoRoot <path> (repeat it or pass several paths to add worktrees outside it).
#     Without -RepoRoot, -Stop stops nothing and says so.
#   - -Stop ends only leftovers whose command line mentions a -RepoRoot path (case-insensitive,
#     "/" and "\" treated alike, whole folder names only: C:\work\app does not match
#     C:\work\app-other). Every other leftover is listed as "not stopped: no link to this
#     repository". A worker whose command line has no path (some pytest workers) is never linked:
#     stop those by hand.
#   - A -RepoRoot must be an existing git repository or worktree folder (it holds .git), and
#     neither a drive root nor the user's home folder: a wider path would link unrelated processes.
# Pass -RepoRoot in the dry run too, so the list says which leftovers are linked.
# The caller (an agent) must show the dry-run list to the user and stop only after the user says yes.
# No prompts here: the script runs under an agent.
param(
    [int]$MinAgeMinutes = 15,
    [string[]]$Names = @('python', 'pythonw', 'node', 'chrome', 'msedge', 'chromedriver', 'pwsh', 'powershell'),
    [switch]$Stop,
    [string[]]$RepoRoot
)

# Compare paths lower-case with backslashes and no trailing slash.
function ConvertTo-PathKey([string]$s) { ($s -replace '/', '\').TrimEnd('\').ToLowerInvariant() }
$roots = @()
foreach ($r in $RepoRoot) {
    if (-not $r) { continue }
    if (-not (Test-Path -LiteralPath $r -PathType Container)) { throw "-RepoRoot '$r' is not an existing folder." }
    $full = (Resolve-Path -LiteralPath $r).ProviderPath
    $key = ConvertTo-PathKey $full
    if (-not (Test-Path -LiteralPath (Join-Path $full '.git'))) { throw "-RepoRoot '$full' is not a git repository or worktree folder (no .git in it)." }
    if ($key -eq (ConvertTo-PathKey ([IO.Path]::GetPathRoot($full))) -or $key -eq (ConvertTo-PathKey $HOME)) {
        throw "-RepoRoot '$full' is a drive root or the home folder: too wide to link processes safely."
    }
    # Whole folder names only: the path must end at a separator, quote, space or the end of the line.
    $roots += '(?<!\w)' + [regex]::Escape($key) + '(?=[\\"''\s]|$)'
}

$all = Get-CimInstance Win32_Process
$alive = @{}
foreach ($p in $all) { $alive[[int]$p.ProcessId] = $true }
$now = Get-Date
$found = @()

foreach ($p in $all) {
    $base = [IO.Path]::GetFileNameWithoutExtension($p.Name)
    if ($Names -notcontains $base) { continue }
    if (-not $p.CreationDate) { continue }
    $age = ($now - $p.CreationDate).TotalMinutes
    if ($age -lt $MinAgeMinutes) { continue }
    $cmd = [string]$p.CommandLine
    # The user's own browser often runs with its parent gone (startup boost); only headless
    # browsers are ever test leftovers.
    if ($base -in @('chrome', 'msedge') -and $cmd -notmatch '--headless') { continue }
    $reason = $null
    if (-not $alive.ContainsKey([int]$p.ParentProcessId)) { $reason = 'parent gone' }
    elseif ($cmd -match '\\\.claude\\worktrees\\(agent-[0-9a-f]+)') {
        $tree = $cmd.Substring(0, $cmd.IndexOf($Matches[1]) + $Matches[1].Length) -replace '^"', ''
        if (-not (Test-Path $tree)) { $reason = 'worktree removed' }
    }
    # An exited process still listed (another program holds its handle) uses no CPU and cannot be stopped.
    if ($reason) {
        $gp = Get-Process -Id $p.ProcessId -ErrorAction SilentlyContinue
        if (-not $gp -or $gp.HasExited) { $reason = $null }
    }
    if ($reason) {
        $key = ConvertTo-PathKey $cmd
        $linked = $false
        foreach ($r in $roots) { if ($key -match $r) { $linked = $true; break } }
        $link = if (-not $roots) { 'unknown (no -RepoRoot)' } elseif ($linked) { 'linked to repository' } else { 'unrelated' }
        $found += [pscustomobject]@{
            Pid = $p.ProcessId; Name = $p.Name; Minutes = [int]$age; Why = $reason; Link = $link
            Cmd = $cmd.Substring(0, [Math]::Min(110, $cmd.Length))
        }
    }
}

# A leftover's own children are leftovers too; stopping the tree root is enough.
if (-not $found) { 'No leftover processes.'; return }
$found | Sort-Object Minutes -Descending | Format-Table -AutoSize | Out-String -Width 220

if (-not $Stop) {
    "Dry run: $($found.Count) leftover(s). Show the list to the user; re-run with -Stop -RepoRoot <path> only after they agree."
    if (-not $roots) { "Pass -RepoRoot <path> to see which leftovers are linked to the repository." }
    return
}
if (-not $roots) {
    "Nothing stopped: -Stop needs -RepoRoot <path> so only processes linked to this repository are ended."
    return
}
$stopped = 0
foreach ($f in $found) {
    if ($f.Link -eq 'linked to repository') {
        & taskkill /PID $f.Pid /T /F 2>$null | Out-Null
        $stopped++
    } else {
        "PID $($f.Pid) $($f.Name): not stopped: no link to this repository"
    }
}
"Stopped $stopped linked process tree(s); $($found.Count - $stopped) left running."
