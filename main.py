import json
import random
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name("config.json")

CATEGORIES = {
    "algorytmy_i_struktury_danych": [
        ("Systemy liczbowe – zakres cyfr i przykłady zapisu.", "Binarny: 0–1 (np. 1010₂), ósemkowy: 0–7 (12₈), dziesiętny: 0–9 (10₁₀), szesnastkowy: 0–9 i A–F (A₁₆)."),
        ("Programowanie strukturalne i niestrukturalne.", "Strukturalne zachowuje uporządkowany przepływ instrukcji i używa m.in. pętli. Niestrukturalne opiera się na skokach do różnych miejsc kodu."),
        ("Rola wskaźników w programowaniu.", "Wskaźnik to zmienna przechowująca adres obiektu w pamięci; pozwala pośrednio odczytywać i modyfikować ten obiekt."),
        ("Rola instrukcji pętli i ich rodzaje.", "Pętla pozwala wielokrotnie wykonać instrukcje. For stosujemy zwykle, gdy znamy liczbę powtórzeń. While działa, dopóki warunek jest prawdziwy. Do while najpierw wykonuje kod, a dopiero potem sprawdza warunek, więc wykona się co najmniej raz."),
        ("Znaczenie asercji początkowej i końcowej algorytmu.", "Asercja początkowa określa warunki wymagane przed uruchomieniem algorytmu, a końcowa – stan gwarantowany po jego zakończeniu."),
        ("Rekurencja ogonowa i bezogonowa.", "W rekurencji ogonowej wywołanie rekurencyjne jest ostatnią operacją funkcji. W bezogonowej po jego powrocie wykonywana jest jeszcze inna operacja."),
        ("Statyczna tablica indeksowana a jednokierunkowa lista związana.", "Tablica ma z góry ustalony rozmiar i szybki dostęp przez indeks. Lista składa się z połączonych węzłów i ułatwia dodawanie oraz usuwanie elementów."),
        ("Algorytmy przeszukiwania drzew binarnych.", "Preorder: korzeń, lewe, prawe poddrzewo. Inorder: lewe, korzeń, prawe. Postorder: lewe, prawe, korzeń."),
        ("Własności dynamicznego stosu LIFO i kolejki FIFO.", "LIFO usuwa jako pierwszy element dodany jako ostatni. FIFO usuwa jako pierwszy element dodany jako pierwszy."),
        ("Złożoność obliczeniowa algorytmów.", "Opisuje zapotrzebowanie algorytmu na czas i pamięć w zależności od rozmiaru danych wejściowych."),
    ],
    "architektura_i_systemy_operacyjne": [
        ("Rodzaje, charakterystyka i przeznaczenie rejestrów procesora.", "Rejestry ogólne przechowują dane i wyniki; licznik rozkazów – adres następnej instrukcji; rejestr instrukcji – bieżącą instrukcję; stosu – szczyt stosu; flag – wynik operacji; adresowe – adresy danych."),
        ("Pamięć wirtualna i tłumaczenie adresu.", "Program korzysta z adresów wirtualnych. Jednostka MMU zamienia je na prawdziwe adresy danych w pamięci RAM. Gdy brakuje miejsca w RAM-ie, system może użyć części dysku jako dodatkowej pamięci."),
        ("Czynniki wpływające na szybkość wykonywania rozkazów.", "M.in. taktowanie, liczba rdzeni i wątków, architektura CPU, cache, szybkość RAM, potokowanie i przewidywanie skoków oraz limity temperatury i mocy."),
        ("Szeregowanie procesów i algorytmy.", "Planista systemu wybiera proces, który w danej chwili otrzyma procesor. Stosuje np. FCFS, SJF, Round Robin lub szeregowanie priorytetowe."),
        ("Synchronizacja procesów i jej metody.", "Kontroluje dostęp do wspólnych danych i zasobów. Służą do tego m.in. mutexy, semafory, sekcje krytyczne, zmienne warunkowe oraz blokady odczytu i zapisu."),
        ("Zakleszczenie procesów i postępowanie.", "Zakleszczenie występuje, gdy procesy wzajemnie czekają na zajęte zasoby. Można mu zapobiegać, unikać go, wykrywać i usuwać albo – zależnie od systemu – ignorować."),
        ("Strategie przydziału segmentów pamięci.", "First Fit wybiera pierwszy pasujący blok, Best Fit – najmniejszy wystarczający, Worst Fit – największy, a Next Fit szuka od miejsca ostatniego przydziału."),
        ("System plików i jego realizacja.", "Organizuje przechowywanie, nazwy, odczyt, zapis i metadane plików. Przykłady: NTFS i FAT32."),
    ],
    "sieci_i_systemy_rozproszone": [
        ("Wyznaczanie trasy przez routing dynamiczny.", "Routery wymieniają informacje, obliczają najlepsze trasy według metryk, zapisują je w tablicach routingu i kierują pakiety do odpowiedniego next hopu."),
        ("RIP a OSPF.", "RIP jest protokołem wektora odległości i używa liczby skoków. OSPF jest protokołem stanu łącza, buduje mapę topologii i wyznacza najkrótsze ścieżki."),
        ("Unikanie kolizji w sieciach przewodowych i bezprzewodowych.", "Klasyczny Ethernet wykrywał kolizje przez CSMA/CD, natomiast Wi‑Fi stara się im zapobiegać przez CSMA/CA."),
        ("Technologie sieci rozległych.", "WAN łączy odległe lokalizacje. Wykorzystuje m.in. łącza operatorów, MPLS, VPN, sieci komórkowe i połączenia satelitarne."),
        ("Stos protokołów TCP/IP.", "To zestaw reguł komunikacji ułożony w warstwy: dostępu do sieci, internetową, transportową i aplikacji."),
        ("Zdalne wywoływanie procedur (RPC).", "Pozwala programowi wywołać funkcję na innym komputerze tak, jakby była lokalna; warstwa RPC obsługuje komunikację i serializację danych."),
    ],
    "programowanie_obiektowe_i_platformy": [
        ("Paradygmat programowania i przykłady.", "To ogólny sposób organizacji programu i myślenia o obliczeniach. Przykłady: imperatywny, obiektowy, funkcyjny, logiczny i zdarzeniowy."),
        ("Klasa w programowaniu obiektowym.", "Klasa jest wzorcem obiektów: definiuje ich stan przez pola lub właściwości oraz zachowanie przez metody."),
        ("Polimorfizm w programowaniu obiektowym.", "Ta sama metoda może działać inaczej dla różnych obiektów. Na przykład metoda wydaj_dzwiek sprawi, że pies zaszczeka, a kot zamiauczy."),
        ("Metody anonimowe i wyrażenia lambda.", "Są krótkimi, nienazwanymi funkcjami, które można przekazywać jako wartości, np. jako argument metody."),
        ("Platforma .NET.", ".NET to platforma do tworzenia i uruchamiania aplikacji, obejmująca środowisko uruchomieniowe, biblioteki i narzędzia; często używa się z nią języka C#."),
    ],
    "grafika_i_multimedia": [
        ("Grafika rastrowa i wektorowa.", "Rastrowa składa się z pikseli i przy powiększaniu traci ostrość. Wektorowa opisuje kształty matematycznie, więc można ją skalować bez utraty jakości."),
        ("Podstawowe pojęcia typografii.", "Krój pisma to projekt liter, font to jego konkretny plik/odmiana, stopień pisma określa rozmiar, interlinia odstęp między wierszami, a wyrównanie sposób ułożenia tekstu."),
        ("Podstawowe formaty plików graficznych.", "JPG – stratne zdjęcia; PNG – bezstratny i przezroczystość; GIF – proste animacje; SVG – grafika wektorowa."),
        ("Etapy tworzenia animacji komputerowej.", "Pomysł i fabuła, storyboard, projektowanie, modelowanie, animowanie, renderowanie oraz montaż i dźwięk."),
        ("Technologie prezentacji scen 3D na stronach internetowych.", "WebGL udostępnia w przeglądarce sprzętowo przyspieszaną grafikę 3D; często korzysta się z bibliotek takich jak Three.js."),
    ],
    "sztuczna_inteligencja": [
        ("Uczenie nadzorowane i samoistne sieci neuronowych.", "Uczenie dostosowuje wagi na podstawie danych i błędu. Nadzorowane używa gotowych odpowiedzi, a nienadzorowane samodzielnie wykrywa wzorce w nieopisanych danych."),
        ("Cele budowania systemów sztucznego życia.", "Służą badaniu, jak powstają i rozwijają się organizmy oraz złożone zachowania; znajdują też zastosowanie w grach, robotyce i AI."),
        ("Własności i zastosowania sterowania rozmytego.", "Logika rozmyta dopuszcza stopnie prawdziwości zamiast tylko prawdy i fałszu. Stosuje się ją m.in. w automatyce, robotyce i sterowaniu pojazdami."),
        ("Drzewo decyzyjne jako reprezentacja wiedzy.", "Reprezentuje decyzje jako węzły z pytaniami, gałęzie z odpowiedziami lub warunkami i liście z wynikami."),
        ("Współczesne zastosowania algorytmów mrówkowych.", "Naśladują odkładanie feromonów przez mrówki i rozwiązują problemy optymalizacyjne, np. wyznaczanie tras, harmonogramów i ścieżek w sieciach."),
    ],
    "bazy_danych": [
        ("Zasady definiujące model danych jako architekturę bazy danych.", "Model danych określa, jak dane są ułożone, jak łączą się ze sobą oraz co można z nimi robić, na przykład dodawać, odczytywać i zmieniać."),
        ("Typy architektonicznych modeli danych.", "Modele: hierarchiczny, sieciowy, relacyjny, dokumentowy i obiektowy."),
        ("Trójpoziomowa architektura systemu baz danych.", "Poziom zewnętrzny opisuje widoki użytkowników, pojęciowy – logiczną strukturę całej bazy, a wewnętrzny – fizyczny sposób przechowywania."),
        ("Istota relacyjnego modelu danych.", "Dane są przechowywane w relacjach przedstawianych jako tabele; wiersze opisują rekordy, kolumny atrybuty, a klucze wiążą tabele."),
        ("Elementy i funkcje jądra systemu zarządzania bazą danych.", "Jądro zarządza plikami i pamięcią, wykonuje zapytania, obsługuje transakcje, współbieżność, odtwarzanie po awarii i integralność danych."),
        ("Metoda blokowania a współbieżne transakcje.", "Blokady chronią dane przed sprzecznymi operacjami równoczesnych transakcji, lecz niewłaściwa kolejność ich pozyskiwania może spowodować zakleszczenie."),
    ],
    "uml_i_inzynieria_oprogramowania": [
        ("Diagramy UML opisujące strukturę systemu.", "Diagram klas, obiektów, komponentów, wdrożenia i pakietów pokazują odpowiednio typy i relacje, instancje, moduły, rozmieszczenie oraz organizację elementów."),
        ("Diagramy UML opisujące zachowanie systemu.", "Należą do nich diagramy przypadków użycia, aktywności, sekwencji, stanów i komunikacji."),
        ("Diagram przypadków użycia UML.", "Pokazuje funkcjonalności systemu z perspektywy użytkownika: aktorów, przypadki użycia oraz relacje między nimi."),
        ("Rodzaje testów w procesie wytwórczym.", "Główne to testy jednostkowe, integracyjne, systemowe i akceptacyjne. Stosuje się też testy regresji, wydajności, bezpieczeństwa i użyteczności."),
        ("Trzy modele cyklu życia systemu.", "Kaskadowy realizuje etapy sekwencyjnie, iteracyjno-przyrostowy buduje kolejne wersje, a spiralny łączy iteracje z analizą ryzyka."),
    ],
    "systemy_wbudowane": [
        ("Elementy niezbędne do budowy systemu wbudowanego.", "Mikrokontroler lub mikroprocesor, pamięć, układy wejścia/wyjścia, zasilanie, czujniki lub elementy wykonawcze oraz oprogramowanie wbudowane."),
        ("Trzy elementy mikrokontrolera.", "Jednostka centralna CPU, pamięć oraz układy wejścia/wyjścia."),
        ("Mikroprocesor a mikrokontroler.", "Mikroprocesor jest głównie CPU i wymaga zewnętrznej pamięci oraz peryferiów. Mikrokontroler integruje CPU, pamięć i wejścia/wyjścia w jednym układzie."),
        ("Konsekwencje stosowania systemów operacyjnych w systemach wbudowanych.", "System operacyjny ułatwia zarządzanie sprzętem i wieloma zadaniami, ale zwiększa zużycie pamięci i energii oraz może pogorszyć przewidywalność czasu reakcji."),
        ("OTP, programowanie w systemie i bootloader.", "OTP to pamięć programowana raz. ISP pozwala wgrywać kod bez wyjmowania układu. Bootloader uruchamia urządzenie i umożliwia załadowanie lub aktualizację właściwego programu."),
    ],
    "spoleczne_etyczne_i_przyszlosciowe_aspekty_informatyki": [
        ("Społeczeństwo informacyjne.", "Społeczeństwo, w którym informacja oraz technologie cyfrowe odgrywają kluczową rolę w pracy, edukacji, komunikacji i życiu codziennym."),
        ("Etyka w informatyce.", "Zasady odpowiedzialnego tworzenia i używania technologii, obejmujące m.in. prywatność, bezpieczeństwo, uczciwość i wpływ społeczny."),
        ("Odpowiedzialność zawodowa informatyków.", "Obejmuje tworzenie bezpiecznych i rzetelnych rozwiązań, przestrzeganie standardów oraz odpowiedzialność za decyzje i błędy."),
        ("Ochrona własności intelektualnej w informatyce.", "Polega na przestrzeganiu praw autorskich, licencji, patentów i praw do znaków towarowych."),
        ("Ochrona prywatności użytkowników technologii.", "Wymaga minimalizacji zbieranych danych, ich zabezpieczania, przejrzystego celu przetwarzania i udostępniania zgodnie z prawem oraz zgodą."),
        ("Ryzyko związane z projektami informatycznymi.", "Obejmuje opóźnienia, przekroczenie budżetu, błędy techniczne, luki bezpieczeństwa, brak zasobów i zmianę wymagań."),
        ("Szkoła w dobie nowoczesnych technologii informacyjnych.", "Technologie wspierają naukę, komunikację i dostęp do materiałów, ale wymagają kompetencji cyfrowych oraz ochrony bezpieczeństwa i prywatności."),
        ("Komputery kwantowe – przyszłość informatyki.", "Wykorzystują kubity i zjawiska kwantowe do wybranych klas problemów. Mogą przyspieszyć specjalistyczne obliczenia, ale nie zastąpią wszystkich komputerów klasycznych."),
        ("Autonomiczne systemy w środowisku społecznym.", "Podejmują decyzje bez ciągłej kontroli człowieka, np. pojazdy autonomiczne; wymagają bezpieczeństwa, przejrzystości i określenia odpowiedzialności."),
        ("Internet rzeczy – zagrożenia i szanse.", "Połączone urządzenia zwiększają automatyzację i wygodę, ale niosą ryzyko wycieku danych, śledzenia i przejęcia słabo zabezpieczonych urządzeń."),
        ("Jak zachować w sieci swoją autonomię?", "Samodzielnie oceniać źródła, świadomie wybierać usługi, kontrolować udostępniane dane, ustawienia prywatności i czas spędzany online."),
        ("Licencje oprogramowania a nowoczesne architektury aplikacji.", "Licencje określają zasady użycia i modyfikacji. Trzeba sprawdzać zgodność licencji bibliotek, komponentów open source, kontenerów i usług chmurowych."),
    ],
}


def load_config():
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"Nie można wczytać config.json: {error}")

    configured = config.get("categories", {})
    unknown = set(configured) - set(CATEGORIES)
    if unknown:
        raise SystemExit(f"Nieznane kategorie w config.json: {', '.join(sorted(unknown))}")
    return config


def get_key(prompt=""):
    print(prompt, end="", flush=True)
    try:
        import msvcrt
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            msvcrt.getwch()
        print()
        return key.lower()
    except ImportError:
        return input().strip().lower()[:1]


def build_pool(config):
    enabled = config.get("categories", {})
    return [
        (category, question, answer)
        for category, entries in CATEGORIES.items()
        if enabled.get(category, False)
        for question, answer in entries
    ]


def main():
    config = load_config()
    pool = build_pool(config)
    if not pool:
        raise SystemExit("Włącz przynajmniej jedną kategorię w config.json.")

    repeat = bool(config.get("repeat_questions", False))
    show_answer = bool(config.get("show_answer_after_key", True))
    remaining = pool.copy()
    number = 0

    print(f"Quiz: {len(pool)} pytań z aktywnych kategorii.")
    print("Klawisze: [Enter/N] następne pytanie, [Q] wyjście.")
    while True:
        if not remaining:
            print("Wszystkie aktywne pytania zostały wykorzystane.")
            break

        category, question, answer = random.choice(pool if repeat else remaining)
        if not repeat:
            remaining.remove((category, question, answer))
        number += 1
        print(f"\n{number}. [{category.replace('_', ' ').title()}]")
        print(question)

        if show_answer:
            key = get_key("Naciśnij dowolny klawisz, aby pokazać odpowiedź (Q – wyjście): ")
            if key == "q":
                break
            print(f"Odpowiedź: {answer}")

        key = get_key("Naciśnij Enter/N, aby wylosować następne pytanie (Q – wyjście): ")
        if key == "q":
            break


if __name__ == "__main__":
    main()
