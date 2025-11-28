# Desired console size (characters, not pixels)
$cols  = 65    # a bit narrower
$lines = 20    # a bit shorter

# --- Set console size ---
mode con cols=$cols lines=$lines | Out-Null

# --- Get position for second monitor (index 1) ---
Add-Type -AssemblyName System.Windows.Forms

$screens = [System.Windows.Forms.Screen]::AllScreens

if ($screens.Count -lt 2) {
    Write-Host "Only one monitor detected; using primary screen." -ForegroundColor Yellow
    $targetScreen = $screens[0]
} else {
    # Second monitor (index 1)
    $targetScreen = $screens[1]
}

$bounds = $targetScreen.Bounds

# Top-left of that monitor
$left = $bounds.X
$top  = $bounds.Y

# --- Move window ---
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", SetLastError=true)]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y,
                                         int nWidth, int nHeight, bool bRepaint);
}
"@

$hwnd = [Win32]::GetForegroundWindow()

# Rough conversion from characters to pixels (tweak if needed)
$charWidth  = 8
$charHeight = 16

$widthPx  = $cols * $charWidth
$heightPx = $lines * $charHeight

[Win32]::MoveWindow($hwnd, $left, $top, $widthPx, $heightPx, $true) | Out-Null

# --- Run your Python panel ---
Set-Location "C:\Users\diogo\weather-forecast-panel"
python main.py