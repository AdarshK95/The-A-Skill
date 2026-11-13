# Remove ONLY what install.ps1 created. Never touches any project's .a\project.md, .a\shared, documentation,
# board, activity files, or the always-on block in instruction files. ~\.a\projects.md (the user's index) is kept.
#   .\uninstall.ps1                       show what would be removed, remove nothing
#   .\uninstall.ps1 -Yes                  global uninstall
#   .\uninstall.ps1 -Project <dir> -Yes   project-level uninstall inside <dir>
param([string]$Project = "", [switch]$Yes)
$ErrorActionPreference = "Stop"
if ($Project) { $Dest = (Resolve-Path $Project).Path; $Global = $false } else { $Dest = $env:USERPROFILE; $Global = $true }
$targets = @((Join-Path $Dest ".a\skills"), (Join-Path $Dest ".a\templates"), (Join-Path $Dest ".a\registry.md"), (Join-Path $Dest ".a\VERSION"), (Join-Path $Dest ".a\SOURCE"))
if ($Global) { $targets += (Join-Path $Dest ".a\commands") }
$globs = @(Join-Path $Dest ".claude\commands\A.*.md")
if (-not $Global) { $globs += (Join-Path $Dest ".github\prompts\A.*.prompt.md") }
$scope = if ($Global) { "global" } else { "project: $Dest" }
Write-Host "The A Skill uninstall ($scope) - would remove:"
$existing = @(); foreach ($t in $targets) { if (Test-Path $t) { $existing += $t } }
foreach ($g in $globs) { Get-ChildItem $g -ErrorAction SilentlyContinue | ForEach-Object { $existing += $_.FullName } }
$existing | ForEach-Object { Write-Host "  $_" }
Write-Host "Kept (yours): every project's .a\project.md, .a\shared\, documentation, board, activity files, instruction-file blocks; ~\.a\projects.md"
if (-not $Yes) { Write-Host "Nothing removed (dry run). Re-run with -Yes to remove the paths above."; exit 0 }
foreach ($p in $existing) { Remove-Item -Recurse -Force $p }
Write-Host "Removed. Start a new chat for the commands to disappear."
