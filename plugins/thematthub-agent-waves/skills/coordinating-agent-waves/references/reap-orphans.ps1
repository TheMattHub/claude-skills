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
#     "/" and "\" treated alike). Every other leftover is listed as
#     "not stopped: no link to this repository".
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
foreach ($r in $RepoRoot) { if ($r) { $roots += ConvertTo-PathKey $r } }

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
        foreach ($r in $roots) { if ($key.Contains($r)) { $linked = $true; break } }
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
