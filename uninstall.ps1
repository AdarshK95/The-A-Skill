# Remove ONLY what install.ps1 created. Never touches any project's .a\project.md, .a\shared, documentation,
# board, activity files, or the always-on block in instruction files. ~\.a\projects.md (the user's index) is kept.
#   .\uninstall.ps1                       show what would be removed, remove nothing
#   .\uninstall.ps1 -Yes                  global uninstall
#   .\uninstall.ps1 -Project <dir> -Yes   project-level uninstall inside <dir>
param([string]$Project = "", [switch]$Yes)
$ErrorActionPreference = "Stop"
if ($Project) { $Dest = (Resolve-Path $Project).Path; $Global = $false } else { $Dest = $env:USERPROFILE; $Global = $true }
$targets = @((Join-Path $Dest ".a\skills"), (Join-Path $Dest ".a\templates"), (Join-Path $Dest ".a\registry.md"), (Join-Path $Dest ".a\VERSION"), (Join-Path $Dest ".a\SOURCE"))
if ($Global) { $targets += (Join-Path $Dest ".a\commands"), (Join-Path $Dest ".a\auto-pointer.md"), (Join-Path $Dest ".copilot\instructions\a-skill.instructions.md") }
$Settings = Join-Path $Dest ".claude\settings.json"
# UTF-8 by name: Windows PowerShell 5.1 would read ANSI and damage non-English characters on write-back.
$hasHook = $Global -and (Test-Path $Settings) -and ([IO.File]::ReadAllText($Settings, [Text.Encoding]::UTF8) -match "auto-pointer\.md")
$globs = @(Join-Path $Dest ".claude\commands\A.*.md")
if (-not $Global) { $globs += (Join-Path $Dest ".github\prompts\A.*.prompt.md") }
$scope = if ($Global) { "global" } else { "project: $Dest" }
Write-Host "The A Skill uninstall ($scope) - would remove:"
$existing = @(); foreach ($t in $targets) { if (Test-Path $t) { $existing += $t } }
foreach ($g in $globs) { Get-ChildItem $g -ErrorAction SilentlyContinue | ForEach-Object { $existing += $_.FullName } }
$existing | ForEach-Object { Write-Host "  $_" }
if ($hasHook) { Write-Host "  the A Skill hook in $Settings (only that entry; backup first)" }
Write-Host "Kept (yours): every project's .a\project.md, .a\shared\, documentation, board, activity files, instruction-file blocks; ~\.a\projects.md"
if (-not $Yes) { Write-Host "Nothing removed (dry run). Re-run with -Yes to remove the paths above."; exit 0 }
foreach ($p in $existing) { Remove-Item -Recurse -Force $p }
if ($hasHook) {   # remove only hooks whose command mentions auto-pointer.md; never print the file (it can hold tokens)
  try {
  Copy-Item -Force $Settings "$Settings.bak-a-skill"
  $raw = [IO.File]::ReadAllText($Settings, [Text.Encoding]::UTF8)
  if ($raw -match '(?m)^\s*(//|/\*)') { throw "settings.json has comments" }   # PowerShell 7 would drop them on write-back
  $s = $raw | ConvertFrom-Json
  $groups = @()
  foreach ($g in @($s.hooks.UserPromptSubmit)) {
    if ($null -eq $g) { continue }
    $kept = @(@($g.hooks) | Where-Object { $_ -and ("$($_.command)" -notlike "*auto-pointer.md*") })
    if ($kept.Count) { $g.hooks = $kept; $groups += $g }
  }
  if ($groups.Count) { $s.hooks.UserPromptSubmit = $groups } else { $s.hooks.PSObject.Properties.Remove('UserPromptSubmit') }
  if (-not @($s.hooks.PSObject.Properties).Count) { $s.PSObject.Properties.Remove('hooks') }
  [IO.File]::WriteAllText($Settings, ($s | ConvertTo-Json -Depth 100), (New-Object Text.UTF8Encoding $false))
  } catch { Write-Host "NOTE: $Settings could not be read as JSON (left untouched); remove the UserPromptSubmit entry mentioning auto-pointer.md by hand." }
}
Write-Host "Removed. Start a new chat for the commands to disappear."
