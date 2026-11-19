# Find (and with -Stop, end) leftover worker processes from agent runs.
# A process is a leftover when its parent process is gone and it is older than -MinAgeMinutes,
# or when its command line points into a worktree folder that no longer exists.
# Default is a dry run: it only lists. Processes whose parent is alive (an MCP server under
# claude.exe, a live pytest run) are never touched.
param(
    [int]$MinAgeMinutes = 15,
    [string[]]$Names = @('python', 'pythonw', 'node', 'chrome', 'msedge', 'chromedriver', 'pwsh', 'powershell'),
    [switch]$Stop
)

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
        $found += [pscustomobject]@{
            Pid = $p.ProcessId; Name = $p.Name; Minutes = [int]$age; Why = $reason
            Cmd = $cmd.Substring(0, [Math]::Min(110, $cmd.Length))
        }
    }
}

# A leftover's own children are leftovers too; stopping the tree root is enough.
if (-not $found) { 'No leftover processes.'; return }
$found | Sort-Object Minutes -Descending | Format-Table -AutoSize | Out-String -Width 220
if ($Stop) {
    foreach ($f in $found) { & taskkill /PID $f.Pid /T /F 2>$null | Out-Null }
    "Stopped $($found.Count) leftover process tree(s)."
} else {
    "Dry run: $($found.Count) leftover(s). Re-run with -Stop to end them."
}
