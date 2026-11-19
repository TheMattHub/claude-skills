# Exports a project's markdown documents to Word and/or PDF. Usage and options: skills/exporting-docs/SKILL.md.
param(
    [string]$ProjectDir = (Get-Location).Path,
    [string[]]$Files,                                   # default: the standard project documents that exist
    [ValidateSet('docx', 'pdf', 'both')][string]$Format = 'docx',
    [string]$Title,                                     # default: project folder name
    [string]$Subtitle = 'Project documentation',
    [string]$Client = '',
    [string]$Author,                                    # default: git user.name
    [string]$Revision = '1.0',
    [string]$RevisionNote = 'First issue',
    [string]$RevisionsFile,                             # YAML with a `revisions:` list (rev, note, date); replaces the single row above
    [string]$Classification = 'unclassified',            # free text, passed to the template unchanged
    [ValidateSet('en', 'it')][string]$Lang = 'en',
    [string]$OutDir,                                    # default: <ProjectDir>\export
    [string]$WordTemplate,                              # default: wordTemplate in ~/.claude/docs-export.json
    [string]$LatexTemplate,                             # default: latexTemplate in ~/.claude/docs-export.json
    [string]$PandocTemplate,                            # default: pandocTemplate in ~/.claude/docs-export.json
    [string]$ConfigPath = "$HOME\.claude\docs-export.json",
    [switch]$Separate,                                  # one output file per document instead of one combined file
    [switch]$HideLinks                                  # PDF: hide link colouring, e.g. for a document meant for print
)
$ErrorActionPreference = 'Stop'

# A session opened before pandoc or mmdc were installed still has the old PATH.
$env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
# Fails with a plain message naming the tool and what needs it, before any work starts.
function Assert-Tool([string]$name, [string]$install, [string]$neededFor) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) { throw "$name not found; it is needed $neededFor. Install it with: $install" }
}
Assert-Tool pandoc 'winget install JohnMacFarlane.Pandoc' 'for every export'

$ProjectDir = (Resolve-Path -LiteralPath $ProjectDir).Path
$cfg = [pscustomobject]@{}
if (Test-Path $ConfigPath) {
    try { $cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json }
    catch { throw "The config file $ConfigPath is not valid JSON (Windows paths need doubled backslashes or forward slashes): $($_.Exception.Message)" }
}
if (-not $WordTemplate) { $WordTemplate = $cfg.wordTemplate }
if (-not $LatexTemplate) { $LatexTemplate = $cfg.latexTemplate }
if (-not $PandocTemplate) { $PandocTemplate = $cfg.pandocTemplate }
# A class without the template that loads it cannot build a PDF; fail before any work. A pandoc template alone is allowed (e.g. one built on a standard class).
if ($LatexTemplate -and -not $PandocTemplate -and $Format -ne 'docx') { throw "latexTemplate is set but pandocTemplate is missing. Add the key pandocTemplate (path to a pandoc LaTeX template that loads the class) to $ConfigPath, or pass -PandocTemplate." }
if (-not $OutDir) { $OutDir = Join-Path $ProjectDir 'export' }
if (-not $Title) { $Title = Split-Path $ProjectDir -Leaf }
if (-not $Author -and (Get-Command git -ErrorAction SilentlyContinue)) { $Author = git -C $ProjectDir config user.name 2>$null }
if (-not $Author) { $Author = $env:USERNAME } # no git, or no user.name set
$date = Get-Date -Format 'dd\/MM\/yyyy' # escaped: a bare '/' becomes the culture's date separator

if (-not $Files) {
    $Files = 'README.md', 'HANDBOOK.md', 'CONCEPTUAL_MODEL.md', 'RESOURCES.md', 'EXPERIMENTS.md', 'DEVLOG.md' |
        Where-Object { Test-Path -LiteralPath (Join-Path $ProjectDir $_) }
}
if (-not $Files) { throw "No markdown documents found in $ProjectDir. Pass -Files." }
$paths = $Files | ForEach-Object { (Resolve-Path -LiteralPath (Join-Path $ProjectDir $_)).Path }

# Tools that only some exports need: checked now, so a missing one fails before the first file is converted.
if ($Format -ne 'docx') {
    $engine = if ($PandocTemplate) { 'pdflatex' } else { 'xelatex' } # the PDF path below uses one or the other
    Assert-Tool $engine 'winget install MiKTeX.MiKTeX' "to build a PDF$(if ($PandocTemplate) { ' with a pandocTemplate' })"
}
$hasMermaid = [bool]($paths | Where-Object { Select-String -LiteralPath $_ -Pattern '^```mermaid' -Quiet })
if ($hasMermaid) { Assert-Tool mmdc 'npm install -g @mermaid-js/mermaid-cli (needs Node.js)' 'to render the Mermaid diagrams in these documents' }

$build = Join-Path $OutDir '.build'
Remove-Item -LiteralPath $build -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $build | Out-Null

# Mermaid needs a browser engine; use the one already on the machine instead of downloading Chromium.
$browser = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', 'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    'C:\Program Files\Google\Chrome\Application\chrome.exe' | Where-Object { Test-Path $_ } | Select-Object -First 1
$puppeteer = Join-Path $build 'puppeteer.json'
if ($hasMermaid -and -not $browser) { throw 'Microsoft Edge or Google Chrome not found; one of them is needed to render the Mermaid diagrams in these documents. Install Edge or Chrome.' }
if ($browser) { @{ executablePath = $browser } | ConvertTo-Json | Set-Content $puppeteer }

# Anchor that pandoc gives a document's first heading, so links between documents work inside the combined file.
function Get-Anchor([string]$path) {
    $h1 = Get-Content -LiteralPath $path | Where-Object { $_ -match '^# ' } | Select-Object -First 1
    if ($h1) { (($h1 -replace '^# ').ToLower() -replace '[^\w\- ]' -replace ' ', '-') }
}

function Convert-Markdown([string]$path, [hashtable]$anchors) {
    $name = [IO.Path]::GetFileNameWithoutExtension($path)
    $text = Get-Content -LiteralPath $path -Raw
    $script:n = 0
    $text = [regex]::Replace($text, '(?ms)^```mermaid[ \t]*\r?\n(.*?)^```[ \t]*\r?$', {
            param($m)
            $script:n++
            $base = "fig-$name-$($script:n)".ToLower()
            Set-Content (Join-Path $build "$base.mmd") $m.Groups[1].Value
            $mmdcArgs = '-i', (Join-Path $build "$base.mmd"), '-o', (Join-Path $build "$base.png"), '-b', 'white', '-s', '2'
            if ($browser) { $mmdcArgs += '-p', $puppeteer }
            $log = & mmdc @mmdcArgs 2>&1
            if (-not (Test-Path (Join-Path $build "$base.png"))) { throw "Mermaid diagram $($script:n) in $name.md failed to render:`n$log" }
            "![]($base.png)"
        })
    # pdflatex runs in the build folder and resolves image paths there, so mirror the project's images into it.
    foreach ($m in [regex]::Matches($text, '!\[[^\]]*\]\(([^)\s]+)\)')) {
        $rel = $m.Groups[1].Value
        $src = Join-Path (Split-Path $path) $rel
        if ($rel -notmatch '^\w+:' -and (Test-Path -LiteralPath $src)) {
            $dst = Join-Path $build $rel
            New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
            Copy-Item -LiteralPath $src -Destination $dst -Force
        }
    }
    [regex]::Replace($text, '\]\(([^)#\s]+\.md)(#[^)]*)?\)', {
            param($m)
            $target = Split-Path $m.Groups[1].Value -Leaf
            if ($anchors.ContainsKey($target)) { "](#$($anchors[$target]))" } else { $m.Value }
        })
}

# Pandoc's Word tables take the "Table" style, which a letterhead template lacks, so they come out without borders.
function Add-TableBorders([string]$docx) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [IO.Compression.ZipFile]::Open($docx, 'Update')
    try {
        $entry = $zip.GetEntry('word/document.xml')
        $reader = [IO.StreamReader]::new($entry.Open()); $xml = $reader.ReadToEnd(); $reader.Dispose()
        $sides = 'top', 'left', 'bottom', 'right', 'insideH', 'insideV' | ForEach-Object { "<w:$_ w:val=`"single`" w:sz=`"4`" w:space=`"0`" w:color=`"808080`"/>" }
        $xml = $xml -replace '<w:tblPr>', "<w:tblPr><w:tblBorders>$($sides -join '')</w:tblBorders>"
        $entry.Delete()
        $writer = [IO.StreamWriter]::new($zip.CreateEntry('word/document.xml').Open()); $writer.Write($xml); $writer.Dispose()
        [regex]::Matches($xml, '<w:tbl>').Count, [regex]::Matches($xml, '<pic:pic[ >]').Count
    }
    finally { $zip.Dispose() }
}

function Export-Set([string[]]$set, [string]$outName, [string]$docTitle) {
    $anchors = @{}
    if ($set.Count -gt 1) { foreach ($p in $set) { $a = Get-Anchor $p; if ($a) { $anchors[(Split-Path $p -Leaf)] = $a } } }
    $break = "`n`n``````{=openxml}`n<w:p><w:r><w:br w:type=`"page`"/></w:r></w:p>`n```````n`n``````{=latex}`n\newpage`n```````n`n"
    $parts = $set | ForEach-Object { Convert-Markdown $_ $anchors }
    $combined = Join-Path $build "$outName.md"
    Set-Content $combined ($parts -join $break)
    $tables = ($parts | ForEach-Object { [regex]::Matches($_, '(?m)^\|[ :|-]*-[ :|-]*\|[ \t]*\r?$').Count } | Measure-Object -Sum).Sum
    # Rendered Mermaid blocks and ordinary markdown images alike.
    $script:figures = ($parts | ForEach-Object { [regex]::Matches($_, '!\[[^\]]*\]\(').Count } | Measure-Object -Sum).Sum
    $common = '-f', 'gfm+raw_attribute', "--resource-path=$build;$ProjectDir", '--toc', '--toc-depth=2',
        "--lua-filter=$PSScriptRoot\table-widths.lua", "--lua-filter=$PSScriptRoot\html-anchors.lua",
        '-M', "title=$docTitle", '-M', "subtitle=$Subtitle", '-M', "author=$Author", '-M', "date=$date"

    if ($Format -in 'docx', 'both') {
        $docx = Join-Path $OutDir "$outName.docx"
        $wordArgs = @($combined) + $common + '-o', $docx
        if ($WordTemplate) { $wordArgs += "--reference-doc=$WordTemplate" }
        & pandoc @wordArgs
        if ($LASTEXITCODE) { throw "pandoc failed for $docx" }
        $t, $i = Add-TableBorders $docx
        "$docx  tables $t of $tables, figures $i of $($script:figures)$(if ($t -ne $tables -or $i -ne $script:figures) { '  <-- CHECK: content lost' })"
    }

    if ($Format -in 'pdf', 'both') {
        $pdf = Join-Path $OutDir "$outName.pdf"
        if ($PandocTemplate) {
            # The class (if any) sets cover, header and footer; the pandoc template feeds it pandoc's body.
            if ($LatexTemplate -like '*.zip') { Expand-Archive -LiteralPath $LatexTemplate -DestinationPath $build -Force }
            elseif ($LatexTemplate) { Copy-Item -Path (Join-Path $LatexTemplate '*') -Destination $build -Recurse -Force }
            # Fixed job name: pdflatex mishandles spaces and '&' in file names.
            $job = 'document'
            $tex = Join-Path $build "$job.tex"
            $latexArgs = @($combined) + $common + '-t', 'latex', '--syntax-highlighting=none', '-o', $tex,
                "--template=$PandocTemplate",
                '-V', "client=$Client", '-V', "revision=$Revision", '-V', "revision-note=$RevisionNote", '-V', "classification=$Classification"
            if ($Lang -eq 'en') { $latexArgs += '-V', 'english=true' }
            if ($HideLinks) { $latexArgs += '-V', 'hidelinks=true' }
            if ($RevisionsFile) { $latexArgs += "--metadata-file=$((Resolve-Path -LiteralPath (Join-Path $ProjectDir $RevisionsFile)).Path)" }
            & pandoc @latexArgs
            if ($LASTEXITCODE) { throw "pandoc failed for $tex" }
            Push-Location $build
            try {
                # Three times: the second run fills the table of contents, which adds pages,
                # so the page total in the footer is right only on the third.
                1..3 | ForEach-Object { $log = & pdflatex -interaction=nonstopmode -halt-on-error "$job.tex" 2>&1 }
                if ($LASTEXITCODE) { throw "pdflatex failed:`n$(($log | Select-String '^!' -Context 0, 3 | Select-Object -First 3) -join "`n")`nFull log: $build\$job.log" }
            }
            finally { Pop-Location }
            Copy-Item (Join-Path $build "$job.pdf") $pdf -Force
            $pages = ([regex]::Match(($log -join "`n"), '\((\d+) pages?')).Groups[1].Value
        }
        else {
            & pandoc @(@($combined) + $common + '-o', $pdf, '--pdf-engine=xelatex')
            if ($LASTEXITCODE) { throw "pandoc failed for $pdf" }
            $pages = '?'
        }
        "$pdf  $pages pages, source has $tables tables and $($script:figures) figures"
    }
}

if ($Separate) { foreach ($p in $paths) { $n = [IO.Path]::GetFileNameWithoutExtension($p); Export-Set @($p) $n "$Title - $n" } }
else { Export-Set $paths ($Title -replace '[\\/:*?"<>|]', '_') $Title }
