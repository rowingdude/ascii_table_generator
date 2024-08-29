# ascii_table_generator
Simple Python Script to turn a CSV into an ASCII table

It takes a CSV such as [addresses.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv) [Thanks FSU]

    First,Last,Street,City,State,ZIP
    John,Doe,120 jefferson st.,Riverside, NJ, 08075
    Jack,McGinnis,220 hobo Av.,Phila, PA,09119
    "John ""Da Man""",Repici,120 Jefferson St.,Riverside, NJ,08075
    Stephen,Tyler,"7452 Terrace ""At the Plaza"" road",SomeTown,SD, 91234
    ,Blankman,,SomeTown, SD, 00298
    "Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,00123


And then we run: ` python.exe tablemaker.py addresses.csv`, and then we get:

    +-----------------------+----------+----------------------------------+-------------+-------+--------+
    |         First         |   Last   |              Street              |     City    | State |  ZIP   |
    +-----------------------+----------+----------------------------------+-------------+-------+--------+
    | John                  | Doe      | 120 jefferson st.                | Riverside   |  NJ   |  08075 |
    | Jack                  | McGinnis | 220 hobo Av.                     | Phila       |  PA   | 09119  |
    | John "Da Man"         | Repici   | 120 Jefferson St.                | Riverside   |  NJ   | 08075  |
    | Stephen               | Tyler    | 7452 Terrace "At the Plaza" road | SomeTown    | SD    |  91234 |
    |                       | Blankman |                                  | SomeTown    |  SD   |  00298 |
    | Joan "the bone", Anne | Jet      | 9th, at Terrace plc              | Desert City | CO    | 00123  |
    +-----------------------+----------+----------------------------------+-------------+-------+--------+

It isn't perfect, but it works!