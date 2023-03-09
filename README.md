# doctor-appointment-app
Appointment system for patients with both the user and admin side.

Baigiamasis CodeAcademy darbas,
Python kursas
Kastancija Gatelytė

Projekte naudojamos bibliotekos:

Tkinter -  GUI
SQLite, SQLalchemy - duomenų bazių informacijos valdymas.
Pillow - paveiksliukų įkėlimas į GUI
Regex - duomenų įvesties tikrinimas
Smtplib - elektroninio pašto jungimas
Requests - prisijungimas prie API

Ligoninės registracijos programa leidžia vartotojui užsiregistruoti sistemoje,  prisijungti  bei užsiregistruoti pas tam tiką gydytoją. Programa leidžia vartotojui matyti savo apsilankymų istoriją Treeview rodinyje, juos trinti, atnaujinti savo informaciją. Programa turi administratoriaus modulį, kuriame administratorius gali valdyti visus duomenis (juos trinti, pridėti, daryti paiešką).

Funkcionalumas:

1. Norėdami prisijungti, turite paspausti mygtuką „Prisijungti“ ir suvesti savo prisijungimo duomenis.
2. Jei norite užsiregistruoti, spauskite mygtuką  “Sukurti naują vartotoją”, suveskite duomenis ir patvirtinkite. Į savo el. paštą gausite registracijos patvirtinimą.
3. Jei pamiršote slaptažodį, spauskite mygtuką “Priminti slaptažodį”, jis bus atsiųstas Jums į elektroninį paštą.
4. Norėdami sukurti naują apsilankymą, prisijungę spauskite mygtuką “Naujas apsilankymas”, suveskite detales ir patvirtinkite. Į savo el. paštą gausite patvirtinimą.
5. Norėdami ištrinti apsilankymą, pažymėkite norimą apsilankymą lentelėje ir spauskite “Trinti apsilankymą”.
6. Norėdami atnaujinti savo informaciją, spauskite “Keisti asmeninę informaciją” mygtuką, suveskite naujus duomenis ir patvirtinkite.
7. Norėdami atnaujinti esamą langą, spauskite mygtuką “Atnaujinti”.
8. Norėdami pamatyti dienos citatą, spauskite mygtuką “Pamatykite dienos citatą!”.
9. Norėdami atsijungti, spauskite mygtuką “Atsijungti.
10. Pagrindiniame puslapyje galite pamatyti ligoninės kontaktus - spauskite mygtuką “Kontaktai”, norėdami grįžti - tiesiog išjunkite langą. Kontaktuose galite naudotis žemėlapiu - jį išdidinti, judinti lange pelės paspaudimu.
11. Norėdami prisijungti kaip administratorius, spauskite “Prisijungti” ir suveskite “admin” ir “admin”.
12. Administratoriaus lange matysite visą ligoninės informaciją apie apsilankymus, pacientus ir daktarus, ją galite redaguoti mygtukų pagalba.
13. Administratoriaus lango meniu (viršuje) rasite paiešką ir atsijungimą.
