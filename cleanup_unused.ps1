# TechnoPath Cleanup Script
# Backs up and removes unused files/folders
# Run with: powershell -ExecutionPolicy Bypass -File cleanup_unused.ps1

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "cleanup_backup_$timestamp"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TechnoPath Cleanup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create backup directory
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Write-Host "📦 Backup directory created: $backupDir" -ForegroundColor Green
Write-Host ""

# Define items to clean up
$foldersToRemove = @(
    "funtion_systems",
    "backend",
    ".aider.tags.cache.v4"
)

$filesToRemove = @(
    # Test/verification scripts
    "backend_django/check_vue.py",
    "backend_django/final_verification.py",
    "backend_django/test_phase1_fixes.py",
    "backend_django/verify_complete.py",
    "backend_django/verify_migration.py",
    "backend_django/verify_setup.py",
    "backend_django/quick_test.py",
    "backend_django/run_tests.py",
    "backend_django/final_check.py",
    "backend_django/test_login.py",
    "backend_django/test_login_simple.py",
    "backend_django/debug_login.py",
    "backend_django/check_login_debug.py",
    
    # Aider artifacts
    ".aider.chat.history.md",
    ".aider.input.history",
    
    # Log files
    "check_out.log",
    "final_out.log",
    "doc_content.txt",
    
    # Unused CSS
    "frontend/src/assets/admin.css",
    
    # Duplicate docs (keep System_Documentation/ versions)
    'Data_Dictionary(Current)',
    'ERD_Entity_Relationship_Diagram(Current)',
    'FDD_Functional_Design_Document(Current)',
    'Use_Case_Diagram_Document(Current)',
    'implementation_plan(V6)',
    
    # Generated HTML reports
    'technopath_codebase_analysis(1).html',
    'technopath_panel2_deep_dive.html',
    'technopath_strategic_ux_analysis.html'
)

$totalSize = 0
$removedCount = 0

# Process folders
Write-Host "📁 Processing Folders..." -ForegroundColor Yellow
foreach ($folder in $foldersToRemove) {
    if (Test-Path $folder) {
        $size = (Get-ChildItem $folder -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($size / 1MB, 2)
        
        # Backup
        $dest = "$backupDir/$folder"
        New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null
        Copy-Item -Path $folder -Destination $dest -Recurse -Force
        
        # Remove
        Remove-Item -Path $folder -Recurse -Force
        Write-Host "  ✅ Removed: $folder ($sizeMB MB)" -ForegroundColor Green
        $totalSize += $size
        $removedCount++
    } else {
        Write-Host "  ⚠️  Not found: $folder" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "📄 Processing Files..." -ForegroundColor Yellow
foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        $sizeKB = [math]::Round($size / 1KB, 2)
        
        # Backup
        $destDir = "$backupDir/$(Split-Path $file -Parent)"
        if ($destDir -and $destDir -ne $backupDir) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        Copy-Item -Path $file -Destination "$backupDir/$file" -Force
        
        # Remove
        Remove-Item -Path $file -Force
        Write-Host "  ✅ Removed: $file ($sizeKB KB)" -ForegroundColor Green
        $totalSize += $size
        $removedCount++
    } else {
        Write-Host "  ⚠️  Not found: $file" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Items removed: $removedCount" -ForegroundColor White
Write-Host "Space freed: $([math]::Round($totalSize / 1MB, 2)) MB" -ForegroundColor White
Write-Host "Backup location: $backupDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "To restore files, copy them from the backup directory." -ForegroundColor Gray
Write-Host "To clean build artifacts (node_modules, dist), run:" -ForegroundColor Gray
Write-Host "  cd frontend && npm install  # Regenerates node_modules" -ForegroundColor Gray
Write-Host "  cd frontend && npm run build  # Regenerates dist" -ForegroundColor Gray
