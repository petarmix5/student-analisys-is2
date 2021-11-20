# Analiza sudjelovanja učenika u nastavi kroz podatake izvezene iz sustava e-Dnevnik

* Projekt stvoren u sklopu kolegija *Inteligentni sustavi 2* na Odjelu za Informatiku, Sveučilište u Rijeci
* Nositelji kolegija: prof. dr. sc. Maja Matetić i mag. educ. math. et inf. Dejan Ljubobratović

Pri izvozu podataka, oni su u Microsoft Excel formatu (.xls) te se takvi spremaju u direktorij `data`. Pandas^1 zatim svaku datoteku smatra *tablicom* nad kojom može izvršavati operacije poput `head(5)` za ispis prvih 5 zapisa tablice, `transform()` za transformaciju vrijednosti određenog stupca i slične.
  
Analiza sudjelovanja učenika u nastavi kroz podatake izvezene iz sustava e-Dnevnik izvedena je kroz:

1. Transformaciju izvezenih podataka
   -  svaki učenik predstavlja jedinstveni **identifikator** retka *tablice*
   -  u početku svaka datoteka predstavlja svoju *tablicu*
   -  rezultat je jedna *tablica* za svaki razred (5.c, 6.c, 7.c)
   -  podatci se **čiste**, nepostojeće vrijednosti se mijenjaju s konstantom 0
   -  rezultirajuća *tablica* sadrži stupce svih triju datotečnih *tablica*:
      -  iz triju datotečnih *tablica* izvlače se stupci i stvara se jedinstvena *tablica* sa sljedećim stupcima:
          ```
            ucenik, vladanje, broj_izostanaka,
            nastup', natjecanje, sportski_dopust,
            srednja_ocjena, opci_uspjeh
          ```
      -  svi se stupci preimenuju po sljedećim pravilima:
         ```
            {
                ' - ': '_',
                '(': '_',
                ')': '',
                ' ': '_',

                'č': 'c',
                'ć': 'c',
                'ž': 'z',
                'š': 's',
                'đ': 'dj',
                'dž': 'dz'
            }
         ```
         gdje se svako pojavljivanje znakova '(' ili ' ' mijenja u znak '_'; zatim 'č' u 'ć' itd.

2. Analizu transformiranih podataka
   - nad podatcima se izvršava Istraživačka analiza podataka (engl. Exploratory Data Analysis - EDA)
   
