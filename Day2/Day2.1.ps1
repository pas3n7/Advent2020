$thepwlist = Get-Content -Path "input.txt"
$numgoodpw = 0


foreach ($i in $thepwlist)
{
    

    $i -match '(?<min>^\d*)-(?<max>\d*)\s(?<letter>[a-z]):\s(?<pw>\w*)' > $null #send to null to quiet the t/f
    $thispw = $Matches.pw
    $thisletter = $Matches.letter
    $thismin = $Matches.min -as [int]
    $thismax = $Matches.max -as [int]


    $numinpw = ($thispw -split $thisletter).count - 1
    
    if($thismin -le $numinpw -and $numinpw -le $thismax)
    {
        $numgoodpw++
    }


}
Write-Output $numgoodpw
