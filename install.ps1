# Install the The A Skill into a project.
# Usage:  .\install.ps1 [-Dest path\to\project]      (default: current directory)
# Idempotent: re-running updates the method and commands, never your project's documents or config.
param([string]$Dest = ".")
$ErrorActionPreference = "Stop"
$Src  = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dest = (Resolve-Path $Dest).Path
Write-Host "Installing The A Skill from $Src into $Dest"

foreach ($d in ".a\skills", ".a\templates", ".claude\commands", ".github\prompts") {
  New-Item -ItemType Directory -Force -Path (Join-Path $Dest $d) | Out-Null
}
Copy-Item -Recurse -Force "$Src\skills\*"    (Join-Path $Dest ".a\skills")
Copy-Item -Recurse -Force "$Src\templates\*" (Join-Path $Dest ".a\templates")
Copy-Item -Force "$Src\registry.md"          (Join-Path $Dest ".a\registry.md")
Copy-Item -Force "$Src\VERSION"              (Join-Path $Dest ".a\VERSION")
Copy-Item -Force "$Src\commands\claude\A.*.md"          (Join-Path $Dest ".claude\commands")
Copy-Item -Force "$Src\commands\copilot\A.*.prompt.md"  (Join-Path $Dest ".github\prompts")

$nSkills  = (Get-ChildItem (Join-Path $Dest ".a\skills") -Recurse -Filter *.md -File).Count
$nClaude  = (Get-ChildItem (Join-Path $Dest ".claude\commands") -Filter "A.*.md" -File).Count
$nCopilot = (Get-ChildItem (Join-Path $Dest ".github\prompts") -Filter "A.*.prompt.md" -File).Count
$ver = (Get-Content (Join-Path $Dest ".a\VERSION")).Trim()
Write-Host "Installed (version $ver):"
Write-Host "  .a\skills                     $nSkills files   (the method)"
Write-Host "  .claude\commands\A.*.md       $nClaude files   (Claude Code: /A.plan, /A.bugfix, ...)"
Write-Host "  .github\prompts\A.*.prompt.md $nCopilot files   (Copilot in VS Code: /A.plan, /A.bugfix, ...)"
Write-Host ""
Write-Host "Open THIS project folder as the workspace root (not a parent folder), start a new chat."
if (-not (Test-Path (Join-Path $Dest ".a\project.md"))) {
  Write-Host "REQUIRED before first use: run /A.init  (creates .a\project.md; nothing works without it)"
} else {
  Write-Host "Config .a\project.md already present; method updated. Run /A.help to check."
}
