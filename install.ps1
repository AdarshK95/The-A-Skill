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
Get-ChildItem "$Src\commands\claude" -Filter "A.*.md" | ForEach-Object {
  (Get-Content $_.FullName -Raw) -replace "\{\{SKILLS_ROOT\}\}", $SkillsRoot | Set-Content (Join-Path $Dest ".claude\commands\$($_.Name)") -NoNewline
}
Get-ChildItem "$Src\commands\copilot" -Filter "A.*.prompt.md" | ForEach-Object {
  (Get-Content $_.FullName -Raw) -replace "\{\{SKILLS_ROOT\}\}", $SkillsRoot | Set-Content (Join-Path $CopilotDir $_.Name) -NoNewline
}

if (Get-ChildItem (Join-Path $Dest ".claude\commands"),$CopilotDir -Filter "A.*" -File | Select-String -Pattern "{{SKILLS_ROOT}}" -List) { throw "A command file still has an unfilled {{SKILLS_ROOT}}; install incomplete." }
$nSkills  = (Get-ChildItem (Join-Path $Dest ".a\skills") -Recurse -Filter *.md -File).Count
$nClaude  = (Get-ChildItem (Join-Path $Dest ".claude\commands") -Filter "A.*.md" -File).Count
$nCopilot = (Get-ChildItem $CopilotDir -Filter "A.*.prompt.md" -File).Count
$ver = (Get-Content (Join-Path $Dest ".a\VERSION")).Trim()
Write-Host "Installed (version $ver, commit $($commit.Substring(0, [Math]::Min(7, $commit.Length)))):"
Write-Host "  $Dest\.a\skills                  $nSkills files   (the method)"
Write-Host "  $Dest\.claude\commands\A.*.md    $nClaude files   (Claude Code: /A.plan, /A.bugfix, ...)"
Write-Host "  $CopilotDir\A.*.prompt.md       $nCopilot files   (Copilot in VS Code)"
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
