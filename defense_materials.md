# Materialy do obrony projektu LiteHD

Dokument przygotowany na podstawie analizy repozytorium LiteHD. Aktywny projekt
znajduje sie w katalogach `backend/`, `frontend/` i `docs/`. Katalog `LiteHD/`
wyglada na zagniezdzona kopie glownych plikow projektu, a pliki ZIP, PPTX i DOCX
sa artefaktami pomocniczymi.

Weryfikacja wykonana podczas analizy:

- backend: `..\.venv\Scripts\python.exe -m unittest discover -s tests` w katalogu
  `backend` - 17 testow, wynik OK,
- frontend: `npm run build` - pierwsza proba zostala zablokowana przez `spawn EPERM`
  dla `esbuild`, druga proba uruchomiona poza sandboxem zakonczyla sie poprawnie.

## A. Krotka analiza projektu

### Nazwa projektu

Nazwa projektu to LiteHD.

Zrodla: `README.md`, `backend/app/main.py`, `frontend/src/config/appInfo.js`.

### Glowny cel aplikacji

LiteHD jest aplikacja typu helpdesk MVP do obslugi zgloszen serwisowych,
zarzadzania klientami, technikami i firmami.

Zrodla: `README.md`, `docs/architecture.md`.

### Problem, ktory projekt rozwiazuje

Projekt porzadkuje proces zglaszania i obslugi problemow technicznych. Umozliwia
rejestracje zgloszenia, przypisanie osoby obslugujacej, zmiane statusu,
prowadzenie historii rozmowy oraz dodawanie zalacznikow.

Zrodla: `README.md`, `backend/app/services/ticket_service.py`.

### Docelowi uzytkownicy

System obsluguje trzy role:

- administrator,
- technik,
- klient.

Role sa jawnie zdefiniowane jako `admin`, `technician` i `client`.

Zrodla: `backend/app/models/user.py`, `docs/architecture.md`.

### Glowne funkcjonalnosci

- logowanie uzytkownikow z rolami,
- tworzenie i przeglad zgloszen,
- statusy `open`, `in_progress`, `closed`,
- priorytety `low`, `medium`, `high`,
- historia odpowiedzi w zgloszeniu,
- zalaczniki `jpg`, `jpeg`, `png`, `txt`, `log`,
- panel administracyjny dla firm, klientow i technikow,
- aktywacja kont przez link i ustawienie hasla.

Zrodla: `README.md`, `backend/app/api/routes/tickets.py`,
`frontend/src/pages/ActivationPage.jsx`.

### Zastosowany stack technologiczny

Backend:

- Python,
- FastAPI,
- SQLAlchemy,
- Alembic,
- PostgreSQL,
- Pydantic,
- JWT,
- bcrypt.

Frontend:

- React 18,
- Vite,
- `@tabler/icons-react`,
- wlasny CSS.

Uruchamianie i infrastruktura lokalna:

- Docker Compose,
- osobne kontenery PostgreSQL, backend i frontend,
- produkcyjny obraz frontendu z Nginx.

Zrodla: `backend/requirements.txt`, `frontend/package.json`,
`docker-compose.yml`, `frontend/Dockerfile`.

### Sposob uruchamiania projektu

Projekt mozna uruchomic przez Docker Compose:

```bash
docker compose up --build
```

Backend mozna uruchomic lokalnie przez srodowisko Python, instalacje zaleznosci,
migracje Alembic i uruchomienie Uvicorn.

Frontend mozna uruchomic lokalnie poleceniami:

```bash
npm install
npm run dev
```

Zrodla: `README.md`, `docker-compose.yml`.

### Najwazniejsze moduly i katalogi

- `backend/app/api/` - trasy HTTP,
- `backend/app/services/` - logika biznesowa,
- `backend/app/repositories/` - dostep do bazy danych,
- `backend/app/models/` - modele SQLAlchemy,
- `backend/app/schemas/` - schematy Pydantic,
- `frontend/src/api/` - wywolania REST,
- `frontend/src/pages/` - widoki stron,
- `frontend/src/components/` - komponenty UI,
- `frontend/src/hooks/` - logika stanu frontendu,
- `docs/` - dokumentacja techniczna projektu.

Zrodla: `docs/architecture.md`, `README.md`.

## B. Architektura projektu

### Architektura wysokiego poziomu

Architektura jest klasyczna i warstwowa. Frontend React komunikuje sie przez REST
API z backendem FastAPI. Backend przechodzi przez warstwy:

```text
api -> services -> repositories -> models -> database
```

Dane sa zapisywane w PostgreSQL przez SQLAlchemy. Migracje schematu obsluguje
Alembic.

Zrodla: `docs/architecture.md`, `backend/app/main.py`,
`backend/alembic/env.py`.

### Frontend

Frontend jest aplikacja React + Vite. Plik `App.jsx` wybiera widok aktywacji,
logowania albo panelu uzytkownika na podstawie sciezki i sesji. Sesja jest
przechowywana w `localStorage`.

Zrodla: `frontend/src/App.jsx`, `frontend/src/api/auth.js`.

### Backend

Backend jest aplikacja FastAPI z routerami dla:

- autoryzacji,
- uzytkownikow,
- klientow,
- firm,
- konfiguracji aplikacji,
- zgloszen.

Dostep jest chroniony przez zaleznosci `get_current_user`, `require_admin_user`
i `require_internal_user`.

Zrodla: `backend/app/main.py`, `backend/app/core/auth.py`.

### Baza danych

Najwazniejsze tabele:

- `users`,
- `activation_tokens`,
- `client_companies`,
- `tickets`,
- `ticket_entries`,
- `ticket_attachments`,
- `app_config`.

Zrodla: `docs/database.md`,
`backend/alembic/versions/20260527_0001_initial_schema.py`.

### Przeplyw danych

Przyklad przeplywu utworzenia zgloszenia:

1. Uzytkownik wypelnia formularz w React.
2. Frontend buduje `FormData` i wysyla `POST /tickets`.
3. Backend odbiera formularz i zalaczniki.
4. `TicketService` ustala wlasciciela zgloszenia.
5. Repozytorium zapisuje zgloszenie w bazie.
6. Zalaczniki sa zapisywane w lokalnym systemie plikow.
7. Metadane zalacznikow trafiaja do bazy.
8. Frontend odswieza liste zgloszen.

Zrodla: `frontend/src/api/tickets.js`,
`backend/app/api/routes/tickets.py`, `backend/app/services/ticket_service.py`.

### Najwazniejsze zaleznosci miedzy komponentami

- `frontend/src/api/*` komunikuje sie z endpointami backendu.
- Routery FastAPI przekazuja prace do serwisow.
- Serwisy uzywaja repozytoriow.
- Repozytoria uzywaja modeli SQLAlchemy i sesji bazy danych.
- Modele SQLAlchemy sa zgodne ze schematem Alembic.
- `docker-compose.yml` laczy PostgreSQL, backend i frontend.

Zrodla: `frontend/src/api`, `backend/app/api/routes`,
`backend/app/services`, `backend/app/repositories`, `docker-compose.yml`.

### Istotne decyzje projektowe i uzasadnienie

1. Cienkie route handlery i logika w serwisach.
   Ulatwia to analize i oddziela HTTP od logiki biznesowej.

2. Repozytoria dla zapytan SQLAlchemy.
   Zapytania do bazy nie sa mieszane z logika API.

3. JWT Bearer dla uwierzytelniania.
   Rozwiazanie jest proste i wystarczajace dla MVP.

4. bcrypt dla hasel.
   Hasla nie sa przechowywane jawnie.

5. Tokeny aktywacyjne zapisywane jako hash.
   Surowa wartosc tokenu nie trafia do bazy danych.

6. Lokalny system plikow dla zalacznikow.
   Rozwiazanie jest proste i latwe do pokazania w projekcie inzynierskim.

7. Prosta nawigacja stanem React zamiast routera.
   Zakres widokow jest niewielki, wiec osobny router nie jest konieczny.

Zrodla: `docs/architecture.md`, `backend/app/core/auth.py`,
`backend/app/services/activation_service.py`,
`backend/app/services/ticket_service.py`, `frontend/src/App.jsx`.

### Potencjalne slabe punkty architektury

- Token jest przechowywany w `localStorage`, co jest proste, ale bardziej podatne
  na skutki XSS niz ciasteczka `HttpOnly`.
  Zrodlo: `frontend/src/api/auth.js`.

- Brak refresh tokenow i uniewazniania sesji po stronie serwera.
  Zrodlo: `docs/architecture.md`.

- Zalaczniki sa przechowywane lokalnie. To ogranicza skalowanie na wiele instancji
  backendu.
  Zrodlo: `backend/app/services/ticket_service.py`, `docs/architecture.md`.

- Walidacja zalacznikow sprawdza rozszerzenie i pusta zawartosc, ale nie widac
  limitu rozmiaru pliku.
  Zrodlo: `backend/app/services/ticket_service.py`.

- Przypisany technik jest zapisywany jako tekst `assignee`, nie jako relacja do
  uzytkownika.
  Zrodlo: `backend/app/models/ticket.py`.

- Lista zgloszen nie ma paginacji po stronie backendu.
  Zrodlo: `backend/app/repositories/ticket_repository.py`.

- Brak CI/CD.
  Brak danych w repozytorium.

- Brak testow frontendowych.
  Brak danych w repozytorium.

- Dokumentacja API opisuje endpointy klientow jako `/users/clients`, a kod i
  frontend uzywaja `/clients`.
  Zrodla: `docs/api.md`, `backend/app/api/routes/clients.py`,
  `frontend/src/api/clients.js`.

## C. Material do obrony

LiteHD to aplikacja helpdeskowa przygotowana jako projekt inzynierski. W repozytorium
jako autor wskazany jest Mateusz Okruch. System sluzy do obslugi zgloszen
serwisowych pomiedzy klientami a zespolem technicznym. Jego celem nie jest pelne
zastapienie duzych systemow ITSM, lecz pokazanie kompletnej, zrozumialej aplikacji
webowej z oddzielnym backendem, frontendem, baza danych, autoryzacja i podstawowym
procesem biznesowym.

Zrodla: `frontend/src/config/appInfo.js`, `docs/architecture.md`.

Motywacja projektu jest uporzadkowanie komunikacji zwiazanej z obsluga problemow
technicznych. Klient moze utworzyc zgloszenie, opisac problem i dodac zalaczniki.
Technik albo administrator moze przejrzec zgloszenie, zmienic jego status,
przypisac osobe obslugujaca oraz prowadzic dalsza korespondencje w historii
zgloszenia. Administrator zarzadza firmami, kontami klientow i kontami technikow.

Zrodla: `README.md`, `frontend/src/pages/DashboardPage.jsx`,
`frontend/src/pages/AdminPage.jsx`.

System wykorzystuje trzy role: administrator, technik i klient. Klient widzi tylko
wlasne zgloszenia, natomiast uzytkownicy wewnetrzni widza szerszy zakres danych.
Ta regula nie opiera sie tylko na adresie e-mail, lecz na powiazaniu zgloszenia
z identyfikatorem uzytkownika `requester_user_id`.

Zrodla: `backend/app/models/user.py`, `backend/app/services/ticket_service.py`.

Backend zostal napisany w FastAPI. Jest podzielony na routery, schematy, serwisy,
repozytoria i modele. Dzieki temu trasy HTTP pozostaja krotkie, logika biznesowa
znajduje sie w serwisach, a zapytania do bazy w repozytoriach. Jest to wazne
w kontekscie pracy inzynierskiej, poniewaz architekture mozna latwo pokazac
i przeanalizowac.

Zrodla: `docs/architecture.md`, `backend/app/main.py`.

Frontend zostal napisany w React i uruchamiany jest przez Vite. Nie zastosowano
rozbudowanego routingu; aplikacja wybiera widok aktywacji, logowania lub panelu
uzytkownika na podstawie sesji i sciezki. Logika zgloszen zostala wydzielona do
hooka `useTicketWorkspace`, a logika administracyjna do `useAdminManagement`.

Zrodla: `frontend/src/App.jsx`, `frontend/src/hooks/useTicketWorkspace.js`,
`frontend/src/hooks/useAdminManagement.js`.

Model danych obejmuje konta uzytkownikow, firmy klientow, tokeny aktywacyjne,
zgloszenia, wpisy w historii zgloszen, zalaczniki i konfiguracje aplikacji.
Schemat bazy jest zarzadzany przez Alembic, a aplikacja uzywa PostgreSQL.

Zrodla: `docs/database.md`,
`backend/alembic/versions/20260527_0001_initial_schema.py`.

Uwierzytelnianie opiera sie na hasle i tokenie JWT. Hasla sa haszowane z uzyciem
bcrypt. Konta klientow i technikow moga byc tworzone bez hasla, a nastepnie
aktywowane przez jednorazowy link. W bazie przechowywany jest hash tokenu
aktywacyjnego, a nie surowy token.

Zrodla: `backend/app/core/auth.py`,
`backend/app/services/activation_service.py`.

Projekt mozna uruchomic przez Docker Compose. Srodowisko sklada sie z PostgreSQL,
backendu i frontendu. Backend przed startem wykonuje migracje Alembic, a frontend
jest dostepny lokalnie przez port 3000. Mozliwe jest tez uruchomienie backendu
i frontendu lokalnie bez Dockera.

Zrodla: `docker-compose.yml`, `README.md`.

Testowanie obejmuje przede wszystkim backend. Sa testy dla logowania, haszowania
hasel, tokenow JWT, aktywacji kont, widocznosci zgloszen klienta, wymuszania
wlasciciela zgloszenia i walidacji zalacznikow. Weryfikacja lokalna wykazala
17 testow zakonczonych wynikiem OK. Frontend ma komende build, ale brak testow
frontendowych w repozytorium.

Zrodla: `backend/tests/test_core_auth.py`,
`backend/tests/test_ticket_service.py`, `README.md`.

Ograniczenia obecnej wersji sa zgodne z charakterem MVP: brak refresh tokenow,
brak uniewazniania sesji, lokalny system plikow dla zalacznikow, brak paginacji
listy zgloszen, brak testow frontendu i brak CI/CD. W rozwoju projektu mozna
dodac paginacje, testy end-to-end, relacje przypisania technika do uzytkownika,
lepsza polityke hasel, object storage dla plikow oraz proces CI.

Zrodla: `docs/architecture.md`, `backend/app/repositories/ticket_repository.py`.

## D. Scenariusz wypowiedzi

Dzien dobry. Chcialbym przedstawic projekt LiteHD, czyli aplikacje helpdeskowa
przygotowana jako projekt inzynierski. Celem projektu bylo stworzenie prostej,
zrozumialej i mozliwej do analizy aplikacji webowej, ktora pokazuje pelny przeplyw
obslugi zgloszen serwisowych: od utworzenia zgloszenia przez klienta, przez
obsluge przez technika, az po administracje uzytkownikami i firmami.

Problem, ktory rozwiazuje aplikacja, polega na uporzadkowaniu komunikacji
technicznej miedzy klientem a zespolem wsparcia. Bez takiego systemu zgloszenia
moga byc rozproszone w wiadomosciach e-mail lub ustaleniach ustnych. LiteHD
centralizuje ten proces: klient opisuje problem, moze dodac zalaczniki, a pracownik
wewnetrzny widzi zgloszenie, moze je przypisac, zmienic status i prowadzic dalsza
rozmowe w historii zgloszenia.

System obsluguje trzy role. Administrator zarzadza firmami, klientami i technikami.
Technik obsluguje zgloszenia. Klient tworzy zgloszenia i widzi tylko wlasne sprawy.
Ta kontrola dostepu jest istotna, poniewaz w systemie helpdesk dane zgloszen moga
dotyczyc problemow konkretnej organizacji. W implementacji dostep klienta jest
oparty na identyfikatorze uzytkownika zapisanym w zgloszeniu, a nie tylko na
adresie e-mail.

Architektura projektu jest podzielona na frontend i backend. Frontend zostal
napisany w React i uruchamiany jest przez Vite. Jest odpowiedzialny za formularze,
liste zgloszen, szczegoly zgloszenia, historie rozmowy i panel administracyjny.
Backend zostal napisany w FastAPI. Zostal podzielony na warstwy: API, schematy
Pydantic, serwisy, repozytoria i modele SQLAlchemy. Dzieki temu routery HTTP sa
krotkie, logika biznesowa znajduje sie w serwisach, a dostep do bazy danych
w repozytoriach.

Baza danych to PostgreSQL. Schemat obejmuje uzytkownikow, firmy klientow, tokeny
aktywacyjne, zgloszenia, wpisy historii, zalaczniki i konfiguracje aplikacji.
Migracje sa obslugiwane przez Alembic. Takie rozwiazanie pozwala jawnie kontrolowac
strukture bazy danych, co jest wazne zarowno technicznie, jak i z punktu widzenia
opisu projektu w pracy.

Uwierzytelnianie opiera sie na tokenach JWT. Hasla sa haszowane przy uzyciu bcrypt.
Dla kont klientow i technikow zastosowano aktywacje przez link. Administrator
tworzy konto bez ustawiania hasla uzytkownikowi, a system generuje link aktywacyjny.
W bazie przechowywany jest hash tokenu, nie jego surowa wartosc. Jezeli SMTP nie
jest skonfigurowane, wiadomosc aktywacyjna trafia do lokalnego katalogu outbox,
co ulatwia prezentacje i testowanie lokalne.

Najwazniejszy przeplyw dzialania wyglada nastepujaco. Uzytkownik loguje sie do
aplikacji. Klient tworzy zgloszenie, podajac tytul, opis i opcjonalne zalaczniki.
Backend zapisuje zgloszenie, wiaze je z kontem klienta i zwraca dane do frontendu.
Technik albo administrator moze otworzyc zgloszenie, zmienic jego status, przypisac
technika i dopisac odpowiedz w historii. Kazda odpowiedz jest zapisywana jako osobny
wpis, a zalaczniki sa przechowywane w systemie plikow z metadanymi w bazie.

Projekt mozna uruchomic przez Docker Compose. Srodowisko sklada sie z kontenera
PostgreSQL, backendu i frontendu. Backend przed startem wykonuje migracje, a
frontend komunikuje sie z API przez sciezke `/api`. Mozliwe jest tez uruchomienie
lokalne bez Dockera, zgodnie z instrukcja w README.

Weryfikacja projektu obejmuje testy jednostkowe backendu. Testy sprawdzaja logowanie,
haszowanie hasel, tokeny JWT, aktywacje kont i wybrane reguly zgloszen. W czasie
analizy uruchomilem 17 testow backendu i zakonczyly sie poprawnie. Frontend zostal
zweryfikowany przez build produkcyjny. Jednoczesnie trzeba uczciwie powiedziec,
ze w repozytorium nie ma testow frontendowych ani konfiguracji CI/CD.

Obecna wersja ma ograniczenia typowe dla MVP. Tokeny JWT nie maja mechanizmu
odswiezania ani uniewazniania sesji po stronie serwera. Zalaczniki sa zapisywane
lokalnie, wiec rozwiazanie nie jest jeszcze przygotowane pod wiele instancji
backendu. Lista zgloszen nie ma paginacji, a przypisany technik jest przechowywany
jako tekst, nie jako relacja do konta uzytkownika. Sa to swiadome uproszczenia,
ktore pozwolily utrzymac projekt prosty i czytelny.

Podsumowujac, LiteHD pokazuje pelny, dzialajacy proces helpdeskowy z podzialem na
role, backendem, frontendem, baza danych, migracjami, autoryzacja, zalacznikami
i aktywacja kont. Najwieksza wartoscia projektu jest czytelna architektura
i mozliwosc latwego wyjasnienia kazdej warstwy systemu. Naturalnym kierunkiem
rozwoju byloby dodanie CI/CD, testow frontendu, paginacji, lepszej obslugi sesji
oraz bardziej produkcyjnej obslugi plikow.

## E. Pytania od komisji

1. **Dlaczego wybrano FastAPI?**

   FastAPI pozwala szybko zbudowac czytelne REST API, dobrze wspolpracuje
   z Pydantic i wymusza jawne typowanie danych wejsciowych oraz wyjsciowych.

2. **Dlaczego React i Vite?**

   React pozwala budowac komponentowy frontend, a Vite upraszcza lokalne
   uruchamianie i build. Projekt nie wymagal ciezszego frameworka.

3. **Dlaczego PostgreSQL?**

   Model jest relacyjny: uzytkownicy, firmy, zgloszenia, wpisy i zalaczniki maja
   jasne relacje. PostgreSQL dobrze pasuje do takiego modelu.

4. **Jak dziala autoryzacja?**

   Backend odczytuje token Bearer JWT, pobiera uzytkownika z bazy i sprawdza jego
   aktywnosc oraz role. Dodatkowe reguly sa w serwisach.

5. **Dlaczego klient widzi tylko swoje zgloszenia?**

   Serwis filtruje zgloszenia po `requester_user_id`. To lepsze niz filtrowanie
   po e-mailu, bo e-mail moze sie zmienic.

6. **Jak zabezpieczono hasla?**

   Hasla sa haszowane przez bcrypt. Kod odrzuca puste albo niepoprawne hashe.

7. **Jak dziala aktywacja konta?**

   System generuje losowy token, zapisuje jego hash w bazie i wysyla link. Po
   ustawieniu hasla konto staje sie aktywne, a token jest oznaczony jako uzyty.

8. **Jak obslugiwane sa zalaczniki?**

   Pliki sa zapisywane lokalnie w `storage/attachments`, a metadane trafiaja do
   tabeli `ticket_attachments`.

9. **Czy projekt jest skalowalny?**

   W obecnej formie umiarkowanie. Backend i baza sa rozdzielone, ale lokalne
   pliki, brak paginacji i brak kolejki zadan ograniczaja skalowanie.

10. **Czy sa testy?**

    Tak, backend ma 17 testow jednostkowych i przeszly poprawnie. Brak danych
    w repozytorium dla testow frontendowych.

11. **Czy jest CI/CD?**

    Brak danych w repozytorium. Nie ma katalogu workflow `.github/`.

12. **Najwieksza trudnosc?**

    Zachowanie prostoty przy jednoczesnym utrzymaniu rol, aktywacji kont,
    zalacznikow i historii zgloszen.

13. **Dlaczego nie uzyto refresh tokenow?**

    Projekt jest MVP. Tokeny maja czas wygasniecia, ale refresh i revocation
    mozna dodac w kolejnej iteracji.

14. **Co zmienic przed wdrozeniem produkcyjnym?**

    Sekrety poza repozytorium, CI/CD, testy frontendu, limity zalacznikow,
    paginacje, monitoring i bardziej bezpieczne przechowywanie sesji.

15. **Czy dokumentacja jest spojna z kodem?**

    W wiekszosci tak, ale znaleziono rozbieznosc: dokumentacja opisuje endpointy
    klientow jako `/users/clients`, a kod uzywa `/clients`.

## F. Najwazniejsze ryzyka podczas obrony

| Ryzyko | Jak powiedziec uczciwie |
|---|---|
| Brak testow frontendu | Backend ma testy jednostkowe, frontend zostal zweryfikowany buildem. Testy komponentow i e2e sa kierunkiem dalszego rozwoju. |
| Brak CI/CD | Repozytorium nie zawiera pipeline'u CI/CD. Projekt jest przygotowany lokalnie i przez Docker Compose. |
| Domyslne hasla i sekret demo | Wartosci w compose sa deweloperskie. README wskazuje, ze nalezy je zastapic prywatnymi wartosciami. |
| Token w `localStorage` | To proste rozwiazanie dla MVP. Produkcyjnie warto rozwazyc ciasteczka `HttpOnly` i ochrone przed XSS. |
| Brak refresh tokenow i revocation | Tokeny wygasaja, ale projekt nie ma serwerowego uniewazniania sesji. To swiadome ograniczenie MVP. |
| Lokalny system plikow dla zalacznikow | Dla jednej instancji jest to proste. Dla skalowania lepszy bylby object storage. |
| Brak paginacji listy zgloszen | Aktualna wersja pobiera liste zgloszen bez paginacji. Dla wiekszych danych nalezaloby dodac paginacje i filtrowanie backendowe. |
| Przypisanie technika jako tekst | To uproszczenie. Docelowo lepsza bylaby relacja do tabeli `users`. |
| Rozbieznosc `docs/api.md` i kodu dla klientow | Dokumentacja wymaga korekty: kod i frontend uzywaja `/clients`, a dokument opisuje `/users/clients`. |
| Brak danych o wdrozeniu produkcyjnym | Brak danych w repozytorium. Projekt pokazuje uruchomienie lokalne i kontenerowe, nie pelne wdrozenie produkcyjne. |

## G. Lista rzeczy do poprawienia przed obrona

### Krytyczne

- Poprawic niespojnosc w `docs/api.md`: endpointy klientow powinny odpowiadac
  kodowi `/clients`.
- Przygotowac czysty scenariusz demonstracyjny: Docker Compose, konto admina,
  dane demo, przykladowe zgloszenie.
- Upewnic sie, ze w publicznej wersji nie ma prywatnych outboxow ani przypadkowych
  danych roboczych.

### Wazne

- Dodac krotka sekcje w dokumentacji o ograniczeniach: localStorage, brak refresh
  tokenow, lokalne zalaczniki, brak paginacji.
- Dodac podstawowe testy frontendu albo przynajmniej opisac brak testow jako
  ograniczenie.
- Dodac prosty workflow CI uruchamiajacy testy backendu i build frontendu.
- Dodac limit rozmiaru zalacznikow i opisac go w API.

### Opcjonalne

- Dodac paginacje zgloszen.
- Zmienic `assignee` na relacje do uzytkownika-technika.
- Rozwazyc object storage dla zalacznikow.
- Rozwazyc refresh tokeny albo sesje w ciasteczkach `HttpOnly`.
- Uporzadkowac artefakty dystrybucyjne: ZIP-y i zagniezdzony katalog `LiteHD/`,
  aby nie mylily komisji podczas przegladu repozytorium.
