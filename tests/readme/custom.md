<!-- common
    $ . "$TESTDIR"/common.sh
-->

    $ arbtt-chart --totals-re='^\(' <<END
    > Tag,Time
    > Act:Work,02:30:00
    > Act:Social,01:20:00
    > Act:Mail,00:20:00
    > Act:Movie,01:30:00
    > (screen),05:40:00
    > 
    > Tag,Time
    > Act:Sport,3600
    > Act:Commute,1800
    > (outside),5400
    > END
    Act                                                                             
    ═══                                                                             
    Work       02:30:00  ████████▓███████▓███▋···÷·······÷········÷·······÷·······÷·
    Movie      01:30:00  ········÷·······÷···▐███▓███████▉········÷·······÷·······÷·
    Social     01:20:00  ········÷·······÷·······÷·······▕████████▓█▊·····÷·······÷·
    Sport      01:00:00  ········÷·······÷·······÷·······÷········÷·▕█████▓██·····÷·
    Commute    00:30:00  ········÷·······÷·······÷·······÷········÷·······÷··████▏÷·
    Mail       00:20:00  ········÷·······÷·······÷·······÷········÷·······÷······█▓▊
                                                                                    
    (screen)   05:40:00  ████████▓███████▓███████▓███████▓████████▓████▊··÷·······÷·
    (outside)  01:30:00  ████████▓███▍···÷·······÷·······÷········÷·······÷·······÷·
