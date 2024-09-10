from Validace import Validator

print("-" * 30)
print(f"{'Evidence pojistenych':>25}")
print("-"* 30)

class Urivatelske_rozhrani():
    """
    Tato třída poskytuje uživatelské rozhraní pro správu pojištěnců. Umožňuje zobrazení menu s různými možnostmi.
    Třída zajišťuje, že uživatel zadá platná data.
    """

    def __init__(self, evidence):
        self.evidence = evidence  # Dependency Injection (vkládání závislostí)

    def nabidka_voleb(self):
        """
        Tato metoda zobrazuje uživateli menu a na základě jeho volby provádí příslušnou akci.
        """

        while True :

            print("Vyberte si akci:")
            print("1 - Pridat nového pojisteného")
            print("2 - Vypsat vsechny pojistené")
            print("3 - Vyhledat pojisteného")
            print("4 - Odebrani pojisteného")
            print("5 - Editace pojisteného")
            print("6 - Konec")

            try:
                volba = int(input())

                match volba:
                    case 1:
                        self.ziskat_platny_vstup()
                        print("Data byla uložena.")
                        self.vypis()
                    case 2:
                        print("=" * 60)
                        pojistenci = self.evidence.vypsat_vsechny_pojistene()
                        for pojistenec in pojistenci:
                            print(pojistenec)
                        self.vypis()
                    case 3:
                        self.ziskani_vstupu_pro_vyhledavani()
                    case 4:
                        self.odstraneni_pojisteneho()
                    case 5:
                        self.editace_pojisteneho()
                    case 6:
                        self.ukonceni_programu()
                    case _:
                        print("Neplatná volba.")

            except ValueError:
                    print("Neplatná volba.")
            except KeyboardInterrupt:
                print("\nProgram byl přerušen. Ukončuji.")
                break

    def ziskat_platny_vstup(self):
        """
        Získává jednotlivé vstupy od uživatele.
        Předává vstupy metodě pridani_pojisteneho.
        Kontroluje zda jméno, příjmení nebo telefonní číslo nejsou duplicitní.
        """
        while True:
            jmeno = Validator.kontrola_delky_a_typu_dat("jméno", pouze_text= True)
            prijmeni = Validator.kontrola_delky_a_typu_dat("příjmení", pouze_text= True)
            telefonni_cislo = Validator.kontrola_delky_a_typu_dat("telefonní číslo",pouze_cisla=True)
            vek = Validator.kontrola_delky_a_typu_dat("věk", pouze_cisla= True)

            for osoba in self.evidence.seznam:
                if (osoba.jmeno.lower() == jmeno.lower() and osoba.prijmeni.lower() == prijmeni.lower()) or \
                        osoba.telefonni_cislo == telefonni_cislo:
                    print(f"Osoba s tímto jménem a příjmením nebo telefonním číslem již existuje.")
                    return
            self.evidence.pridani_pojisteneho(jmeno, prijmeni, telefonni_cislo, vek)
            return


    def ziskani_vstupu_pro_vyhledavani(self):
        """
        Získává vstup pro metodu vyhledání pojištěného a odebrani pojisteneho.
        """

        hledane_jmeno = input("Zadejte jméno osoby:\n").strip()
        hledane_prijmeni = input("Zadejte příjmení osoby:\n").strip()
        nalezena_osoba = self.evidence.vyhledani_pojisteneho(hledane_jmeno, hledane_prijmeni)
        if nalezena_osoba:
            print(f"Nalezena osoba: {nalezena_osoba}")
            self.vypis()
            return hledane_jmeno,hledane_prijmeni
        else:
            print(f"Osoba {hledane_jmeno} {hledane_prijmeni} nebyla nalezena.")
        self.vypis()
        return None,None

    def editace_pojisteneho(self):

        """
        Umožňuje editaci údajů pojištěného. Uživatel zadá jméno a příjmení pro vyhledání osoby,
        a pokud je nalezena, může upravit její údaje, jako je jméno, příjmení, telefonní číslo a věk.
        """

        jmeno,prijmeni = self.ziskani_vstupu_pro_vyhledavani()
        nalezena_osoba = self.evidence.vyhledani_pojisteneho(jmeno,prijmeni)

        if nalezena_osoba:
            while True:

                print("Co chcete upravit?")
                print("1 - Jméno")
                print("2 - Příjmení")
                print("3 - Telefonní číslo")
                print("4 - Věk")
                print("5 - Ukončit úpravy")

                try:
                    volba = int(input())

                    match volba:
                        case 1:
                            nove_jmeno = Validator.kontrola_delky_a_typu_dat("nové jméno", pouze_text=True)
                            nalezena_osoba.jmeno = nove_jmeno
                            print(f"Jméno bylo změněno na {nove_jmeno}.")
                        case 2:
                            nove_prijmeni = Validator.kontrola_delky_a_typu_dat("nové příjmení", pouze_text=True)
                            nalezena_osoba.prijmeni = nove_prijmeni
                            print(f"Příjmení bylo změněno na {nove_prijmeni}.")
                        case 3:
                            nove_tel_cislo = Validator.kontrola_delky_a_typu_dat("nové telefonní číslo", pouze_cisla=True)
                            nalezena_osoba.telefonni_cislo = nove_tel_cislo
                            print(f"Telefonní číslo bylo změněno na {nove_tel_cislo}.")
                        case 4:
                            novy_vek = Validator.kontrola_delky_a_typu_dat("nový věk", pouze_cisla=True)
                            nalezena_osoba.vek = novy_vek
                            print(f"Věk byl změněn na {novy_vek}.")
                        case 5:
                            print("Upravy byly ukončeny.\n")
                            break
                        case _:
                            print("Neplatná volba.")
                except ValueError:
                    print("Neplatná volba.")
                except KeyboardInterrupt:
                    print("\nProgram byl přerušen. Ukončuji.")
                    break

    def odstraneni_pojisteneho(self):

        jmeno, prijmeni = self.ziskani_vstupu_pro_vyhledavani()

        if jmeno and prijmeni:
            if self.potvrdit_akci(f"Opravdu chceš odebrat pojištěného {jmeno} {prijmeni}?"):
                odstranena_osoba = self.evidence.odebrani_pojisteneho(jmeno, prijmeni)
                if odstranena_osoba:
                    print(f"Osoba {jmeno} {prijmeni} byla úspěšně odstraněna.")
                else:
                    print(f"Osoba {jmeno} {prijmeni} nebyla nalezena.")
                self.vypis()

    def ukonceni_programu(self):
        if self.potvrdit_akci("Opravdu chceš ukončit program?"):
            print("Program byl úspěšně ukončen.")
            exit()

    def potvrdit_akci(self, zprava):
        """
        Zobrazí zprávu kterou předa jina metoda a požádá uživatele o potvrzení akce.
        """
        while True:
            odpoved = input(f"\n{zprava} ano / ne: ").lower()
            if odpoved == "ano":
                return True
            elif odpoved == "ne":
                return False
            else:
                print("Neplatný příkaz, musíte zadat ano / ne")

    def vypis(self):
        print()
        print()
        print("Pokračujte libovolnou klavesou")
        input()