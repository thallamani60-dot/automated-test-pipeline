$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$demoTest = Join-Path $projectRoot "tests\test_ci_failure_demo.py"
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    $python = "python"
}

try {
    @'
from app.utils import safe_divide


def test_intentionally_wrong_expectation():
    assert safe_divide(8, 2) == 5
'@ | Set-Content -LiteralPath $demoTest -Encoding utf8

    Write-Host "Step 1: run a test with an intentionally incorrect expected value."
    Push-Location $projectRoot
    try {
        & $python -m pytest tests/test_ci_failure_demo.py -q
        $failureExitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($failureExitCode -eq 0) {
        throw "The intentional failure unexpectedly passed."
    }
    Write-Host "Expected result observed: pytest exited with code $failureExitCode."

    @'
from app.utils import safe_divide


def test_corrected_expectation():
    assert safe_divide(8, 2) == 4
'@ | Set-Content -LiteralPath $demoTest -Encoding utf8

    Write-Host "Step 2: correct the expected value and rerun the test."
    Push-Location $projectRoot
    try {
        & $python -m pytest tests/test_ci_failure_demo.py -q
        $successExitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($successExitCode -ne 0) {
        throw "The corrected demonstration test failed with code $successExitCode."
    }
    Write-Host "Resolution confirmed: pytest exited with code 0."
}
finally {
    Remove-Item -LiteralPath $demoTest -ErrorAction SilentlyContinue
}
