<!-- common
    $ . "$TESTDIR"/common.sh
-->

    $ arbtt-chart <<END
    > Tag,Time
    > Screen:Work,02:30:00
    > Screen:Social,01:20:00
    > Screen:Mail,00:20:00
    > Screen:Movie,01:30:00
    > (total time),05:40:00
    > 
    > Tag,Time
    > Outside:Sport,3600
    > Outside:Commute,1800
    > (total time),5400
    > END
    Screen                                                                          
    ══════                                                                          
    Work          02:30:00  █████████▓█████████▓████▊····÷·········÷·········÷······
    Movie         01:30:00  ·········÷·········÷····▐████▓█████████▍·········÷······
    Social        01:20:00  ·········÷·········÷·········÷·········▐█████████▓██▊···
    Mail          00:20:00  ·········÷·········÷·········÷·········÷·········÷··▐██▉
                                                                                    
    (total time)  05:40:00  █████████▓█████████▓█████████▓█████████▓█████████▓██████
                                                                                    
    Outside                                                                         
    ═══════                                                                         
    Sport         01:00:00  █████████▓·········÷·········÷·········÷·········÷······
    Commute       00:30:00  ·········▕████▊····÷·········÷·········÷·········÷······
                                                                                    
    (total time)  01:30:00  █████████▓████▉····÷·········÷·········÷·········÷······
