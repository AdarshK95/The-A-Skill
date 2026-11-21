# Install The A Skill. Default: once per machine (global). Then run /A.project.start in each folder you want as a project.
#   .\install.ps1                    global: method in ~\.a, commands in ~\.claude\commands and ~\.a\commands\copilot
#   .\install.ps1 -Project <dir>     project-level: everything inside <dir> (for a repository that must carry the method)
# Idempotent: re-running updates the method and commands, never a project's documents or config.
param([string]$Project = "")
$ErrorActionPreference = "Stop"
# Where this repository is: the script's folder, or the current folder when run as a script block (managed machines).
$Src = if ($PSScriptRoot) { $PSScriptRoot } elseif ($MyInvocation.MyCommand.Path) { Split-Path -Parent $MyInvocation.MyCommand.Path } else { (Get-Location).Path }
if (-not (Test-Path (Join-Path $Src "skills\core\SKILL.md"))) { throw "Run this from the cloned The-A-Skill folder (skills\core\SKILL.md not found under $Src)." }
if ($Project) {
  $Dest = (Resolve-Path $Project).Path; $Global = $false
  $SkillsRoot = ".a/skills"; $CopilotDir = Join-Path $Dest ".github\prompts"
} else {
  $Dest = $env:USERPROFILE; $Global = $true
  $SkillsRoot = (Join-Path $Dest ".a\skills") -replace "\\","/"; $CopilotDir = Join-Path $Dest ".a\commands\copilot"
}
foreach ($d in (Join-Path $Dest ".a\skills"), (Join-Path $Dest ".a\templates"), (Join-Path $Dest ".claude\commands"), $CopilotDir) {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
}
Write-Host "Installing The A Skill from $Src into $Dest"

Copy-Item -Recurse -Force "$Src\skills\*"    (Join-Path $Dest ".a\skills")
Copy-Item -Recurse -Force "$Src\templates\*" (Join-Path $Dest ".a\templates")
Copy-Item -Force "$Src\install.sh","$Src\install.ps1","$Src\uninstall.sh","$Src\uninstall.ps1" (Join-Path $Dest ".a\templates")
Copy-Item -Force "$Src\registry.md"          (Join-Path $Dest ".a\registry.md")
Copy-Item -Force "$Src\VERSION"              (Join-Path $Dest ".a\VERSION")
$scope = if ($Global) { "global" } else { "project" }
$commit = "unknown"; try { $commit = (git -C $Src rev-parse HEAD 2>$null).Trim(); if (-not $commit) { $commit = "unknown" } } catch {}
"repository: https://github.com/AdarshK95/The-A-Skill`ninstalled: $(Get-Date -Format 'dd MMM yy, hh:mm tt')`nscope: $scope`ncommit: $commit" | Set-Content (Join-Path $Dest ".a\SOURCE")
if ($Global -and -not (Test-Path (Join-Path $Dest ".a\projects.md"))) { Copy-Item "$Src\templates\projects.md" (Join-Path $Dest ".a\projects.md") }
if (-not (Test-Path (Join-Path $Dest ".a\settings.md"))) { Copy-Item "$Src\templates\settings.md" (Join-Path $Dest ".a\settings.md") }
Get-ChildItem (Join-Path $Dest ".claude\commands") -Filter "A.*.md" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem $CopilotDir -Filter "A.*.prompt.md" -ErrorAction SilentlyContinue | Remove-Item -Force
# Every text read and write is UTF-8 (no byte-order mark) by name: Windows PowerShell 5.1 would otherwise read ANSI and PowerShell 7 UTF-8.
function Read-Utf8([string]$Path) { [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8) }
function Write-Utf8([string]$Path, [string]$Text) { [IO.File]::WriteAllText($Path, $Text, (New-Object Text.UTF8Encoding $false)) }
Get-ChildItem "$Src\commands\claude" -Filter "A.*.md" | ForEach-Object {
  Write-Utf8 (Join-Path $Dest ".claude\commands\$($_.Name)") ((Read-Utf8 $_.FullName) -replace "\{\{SKILLS_ROOT\}\}", $SkillsRoot)
}
Get-ChildItem "$Src\commands\copilot" -Filter "A.*.prompt.md" | ForEach-Object {
  Write-Utf8 (Join-Path $CopilotDir $_.Name) ((Read-Utf8 $_.FullName) -replace "\{\{SKILLS_ROOT\}\}", $SkillsRoot)
}

if (Get-ChildItem (Join-Path $Dest ".claude\commands"),$CopilotDir -Filter "A.*" -File | Select-String -Pattern "{{SKILLS_ROOT}}" -List) { throw "A command file still has an unfilled {{SKILLS_ROOT}}; install incomplete." }

# On by default (global only): a pointer every message starts with, so a message with no /A.* command runs auto mode.
# ponytail: project-level installs get no hook (no path that works for every clone); their always-on block stays at the top of CLAUDE.md instead.
$HookNote = "not added (project-level install)"
if ($Global) {
  $Pointer = (Join-Path $Dest ".a\auto-pointer.md") -replace "\\","/"
  $PointerTemplate = Read-Utf8 "$Src\templates\auto-pointer.md"
  # The pointer is printed by a shell before every message; plain ASCII survives every shell's output encoding.
  # ponytail: only the template is checked; a non-ASCII user folder name can still show garbled in the path on Windows PowerShell 5.1 (cosmetic; the instructions stay readable).
  if ($PointerTemplate -match '[^\x00-\x7F]') { throw "templates\auto-pointer.md has non-ASCII characters; the hook output would be garbled on some shells." }
  $PointerText = $PointerTemplate -replace "\{\{SKILLS_ROOT\}\}", $SkillsRoot
  Write-Utf8 $Pointer $PointerText
  $CopilotInstr = Join-Path $Dest ".copilot\instructions"
  New-Item -ItemType Directory -Force -Path $CopilotInstr | Out-Null
  Write-Utf8 (Join-Path $CopilotInstr "a-skill.instructions.md") "---`napplyTo: '**'`ndescription: The A Skill is the default workflow`n---`n`n$PointerText"
  # The hook names its shell: PowerShell exists on every Windows machine, Git Bash may not. Exits 0 either way;
  # a missing pointer says so on every message instead of switching the skill off silently.
  $HookCmd = "`$p = '$Pointer'; if (Test-Path -LiteralPath `$p) { Get-Content -LiteralPath `$p -Raw } else { 'The A Skill: pointer file missing (' + `$p + '). Run /A.skill.repair.' }"
  # Merge the hook into ~/.claude/settings.json. Never print that file: it can hold tokens.
  $Settings = Join-Path $Dest ".claude\settings.json"
  New-Item -ItemType Directory -Force -Path (Split-Path $Settings) | Out-Null
  try {
    $raw = if (Test-Path $Settings) { Read-Utf8 $Settings } else { "" }
    # PowerShell 7 parses // and /* */ comments and would drop them on write-back: leave such a file alone.
    # ponytail: catches comments that start a line, not ones trailing a value; a strict JSON parser is the upgrade.
    if ($raw -match '(?m)^\s*(//|/\*)') { throw "settings.json has comments" }
    $s = if ([string]::IsNullOrWhiteSpace($raw)) { [pscustomobject]@{} } else { $raw | ConvertFrom-Json }
    if (Test-Path $Settings) { Copy-Item -Force $Settings "$Settings.bak-a-skill" }
    if (-not $s.PSObject.Properties['hooks']) { $s | Add-Member -NotePropertyName hooks -NotePropertyValue ([pscustomobject]@{}) }
    $groups = @()
    foreach ($g in @($s.hooks.UserPromptSubmit)) {   # drop an older A Skill hook, keep everything else
      if ($null -eq $g) { continue }
      $kept = @(@($g.hooks) | Where-Object { $_ -and ("$($_.command)" -notlike "*auto-pointer.md*") })
      if ($kept.Count) { $g.hooks = $kept; $groups += $g }
    }
    $groups += [pscustomobject]@{ hooks = @([pscustomobject]@{ type = "command"; shell = "powershell"; command = $HookCmd }) }
    if ($s.hooks.PSObject.Properties['UserPromptSubmit']) { $s.hooks.UserPromptSubmit = $groups } else { $s.hooks | Add-Member -NotePropertyName UserPromptSubmit -NotePropertyValue $groups }
    Write-Utf8 $Settings ($s | ConvertTo-Json -Depth 100)
    $HookNote = "added (UserPromptSubmit in $Settings; backup $Settings.bak-a-skill)"
  } catch { $HookNote = "NOT added: $Settings could not be read as JSON (left untouched); add it by hand (SETUP.md)" }
}
$Detected = "PowerShell $($PSVersionTable.PSVersion.Major).$($PSVersionTable.PSVersion.Minor) ($($PSVersionTable.PSEdition)); Python: not needed" + $(if ($Global) { "; hook shell: powershell" } else { "" })
$nSkills  = (Get-ChildItem (Join-Path $Dest ".a\skills") -Recurse -Filter *.md -File).Count
$nClaude  = (Get-ChildItem (Join-Path $Dest ".claude\commands") -Filter "A.*.md" -File).Count
$nCopilot = (Get-ChildItem $CopilotDir -Filter "A.*.prompt.md" -File).Count
$ver = (Get-Content (Join-Path $Dest ".a\VERSION")).Trim()
Write-Host "Installed (version $ver, commit $($commit.Substring(0, [Math]::Min(7, $commit.Length)))):"
Write-Host "  $Dest\.a\skills                  $nSkills files   (the method)"
Write-Host "  $Dest\.claude\commands\A.*.md    $nClaude files   (Claude Code: /A.plan, /A.bugfix, ...)"
Write-Host "  $CopilotDir\A.*.prompt.md       $nCopilot files   (Copilot in VS Code)"
Write-Host "  On by default (auto mode every message): Claude Code hook $HookNote"
Write-Host "  Detected: $Detected"
if ($Global) { Write-Host "                                   Copilot: $CopilotInstr\a-skill.instructions.md" }
Write-Host ""
if ($Global) {
  Write-Host "INSTALLATION COMPLETE. The A Skill $ver is installed for this machine (global)."
  Write-Host ""
  Write-Host "To see the /A.* shortcuts in VS Code (Copilot), two steps remain:"
  Write-Host "  1. Settings -> chat.promptFilesLocations -> add: $CopilotDir"
  Write-Host "  2. Developer: Reload Window"
  Write-Host "  3. The IDE will ask before reading the method files (they live in $Dest\.a, outside your workspace)."
  Write-Host "     Agents: follow $Dest\.a\skills\core\references\ide-permissions.md - search the IDE settings for a permanent"
  Write-Host "     allowance first; if none, test the prompt once with the user; if still nothing permanent, offer a local mirror of the method inside the workspace. Ask before each change."
  Write-Host "Claude Code needs nothing. (Agents: ask the user for approval, do 1 and 2, confirm /A.help appears, then do 3.)"
  Write-Host ""
  Write-Host "The skill remembers work PER PROJECT: in any folder you want to work in, run /A.project.start once."
  Write-Host "Everything done there (board, logs, decisions) becomes that project's memory, separate from every other project. /A.project.list shows them all."
} else {
  Write-Host "This was a PROJECT-LEVEL install into $Dest`: the commands are read from this folder, so it must be the workspace root for them to appear (the global install has no such limit)."
  Write-Host "Open this folder, start a new chat, and run /A.project.start (required; nothing is remembered without it)."
}
