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

Write-Host "Installed:"
Write-Host "  .a\skills, .a\templates, .a\registry.md         (the method)"
Write-Host "  .claude\commands\A.*.md                          (Claude Code: /A.plan, /A.bugfix, ...)"
Write-Host "  .github\prompts\A.*.prompt.md                    (Copilot in VS Code: /A.plan, /A.bugfix, ...)"
Write-Host ""
if (-not (Test-Path (Join-Path $Dest ".a\project.md"))) {
  Write-Host "Next: open the project in your agent, start a new chat, and run /A.init"
} else {
  Write-Host "Config .a\project.md already present; method updated. Run /A.help to check."
}
