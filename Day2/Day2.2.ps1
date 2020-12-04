$thepwlist = Get-Content -Path ".\Day2\input.txt"
$numgoodpw = 0


foreach ($i in $thepwlist)
{
    

    $i -match '(?<num1>^\d*)-(?<num2>\d*)\s(?<letter>[a-z]):\s(?<pw>\w*)' > $null #send to null to quiet the t/f
    $thispw = $Matches.pw
    $thisletter = $Matches.letter
    $thisnum1 = $Matches.num1 -as [int]
    $thisnum2 = $Matches.num2 -as [int]


	if($thispw[$thisnum1 - 1] -eq $thisletter -xor $thispw[$thisnum2 -1] -eq $thisletter)
	{
		$numgoodpw++
	}
}

Write-Output $numgoodpw