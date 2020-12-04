$inputreport = @()
$inputreport = Get-Content -Path "input.txt" 

$inputreportints = @()
$theproduct

foreach ($i in $inputreport)
{
    $inputreportints += $i -as [int];
}

foreach ($i in $inputreportints)
{
    if($inputreportints.Contains(2020 - $i))
    {
        
     $theproduct = ($i * (2020 - $i))
     
     Write-Output $i
     Write-Output $theproduct
     break
     }
}
