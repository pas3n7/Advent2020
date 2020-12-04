$inputreport = @()
$inputreport = Get-Content -Path "input.txt" 

$inputreportints = @()
$theproduct

foreach ($i in $inputreport)
{
    $inputreportints += $i -as [int];
}



while(!$theproduct)
{
    $thissum = 0
    $thenumbers = $inputreportints | Get-Random -Count 3
    #I got a little too obsessed with optimizing, then decided to do this the worst way I could think of.

    foreach ($i in $thenumbers)
    {
        $thissum += $i
    }



    if ((($thenumbers | Sort-Object | Get-Unique).count -eq 3) -and ($thissum -eq 2020))
    {
        $theproduct = $thenumbers[0]*$thenumbers[1]*$thenumbers[2]
        Write-Output "The Product: " $theproduct
        Write-Output "The Numbers: " $thenumbers

    }

}
