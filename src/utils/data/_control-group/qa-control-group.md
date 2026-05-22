# QA Control Group

Simple client-facing Q/A list grouped by category.

---

## calendar-scheduling-booking

---

### Q/A 1

**Q:**

V online objednávání nejsou vidět volné termíny, i když je v kalendáři máme. Co zkontrolovat?

**A:**

Zkontrolujte, zda je kalendář publikovaný pro online objednávání, má nastavenou pracovní dobu, správný typ návštěvy a termíny nejsou blokované výjimkou nebo obsazeností zdroje.

---

### Q/A 2

**Q:**

Pacienti se nemohou objednat na časy, kdy ordinujeme. Kde bývá chyba?

**A:**

Obvykle v pracovní době kalendáře, dostupnosti zdroje nebo pravidlech pro online zobrazení. Upravte ordinační dobu a ověřte, zda je povolený odpovídající typ objednávky.

---

### Q/A 3

**Q:**

Rezervace termínu nejde dokončit. Co může být špatně?

**A:**

Zkontrolujte povinná pole objednávkového formuláře, dostupnost vybraného termínu, konflikt v kalendáři a nastavení služby nebo typu návštěvy.

---

### Q/A 4

**Q:**

Pro určitý typ návštěvy se nenabízí žádné termíny. Jak to opravit?

**A:**

Ověřte, že je typ návštěvy povolený pro daný kalendář nebo zdroj, má nastavenou délku slotu a spadá do publikované pracovní doby.

---

### Q/A 5

**Q:**

V kalendáři vznikají překryvy objednávek. Co nastavit?

**A:**

Zkontrolujte délku slotů, kapacitu zdroje, pravidla konfliktů a to, zda se objednávky zapisují do správného kalendáře nebo místnosti.

---

### Q/A 6

**Q:**

Uživatel nevidí kalendář, se kterým má pracovat. Čím to bývá?

**A:**

Nejčastěji oprávněním role, nepřiřazením ke kalendáři nebo aktivním filtrem v aplikaci. Zkontrolujte roli, přiřazení zdroje a zobrazené filtry.

---

### Q/A 7

**Q:**

Online objednávka se nepromítne do interního kalendáře. Co prověřit?

**A:**

Prověřte propojení online objednávání s interním kalendářem, cílový kalendář, stav synchronizace a případné validační chyby u objednávky.

---

### Q/A 8

**Q:**

Konkrétní termín nejde vybrat, ale není obsazený. Co může být příčinou?

**A:**

Termín může být blokovaný výjimkou, mimo publikovanou pracovní dobu, nepovolený pro daný typ návštěvy nebo omezený kapacitou zdroje.

---

### Q/A 9

**Q:**

Připomínky objednaných termínů se neodesílají. Co mám zkontrolovat?

**A:**

Zkontrolujte, zda jsou připomínky zapnuté, mají správnou šablonu, nastavený čas odeslání a dostupný komunikační kanál.

---

### Q/A 10

**Q:**

V rezervačním formuláři chybí nebo nesedí údaje. Kde se to nastavuje?

**A:**

Zkontrolujte nastavení objednávkového formuláře, povinná pole, mapování na typ návštěvy a pravidla zobrazení pro online objednávání.

---

## certificate-authentication-setup

---

### Q/A 1

**Q:**

Při přihlášení se mi nenabízí správný certifikát. Co mám zkontrolovat?

**A:**

Ověřte, že je certifikát nainstalovaný ve správném uživatelském úložišti, je platný, má dostupný soukromý klíč a aplikace nebo prohlížeč běží pod profilem, kde je certifikát uložený.

---

### Q/A 2

**Q:**

Aplikace hlásí problém s platností certifikátu. Co to obvykle znamená?

**A:**

Certifikát může být prošlý, nahrazený novým, nedůvěryhodný nebo použitý pro jiný účel. Zkontrolujte datum platnosti, vydavatele a zda je vybraný certifikát určený pro danou službu.

---

### Q/A 3

**Q:**

Dokument nebo požadavek nejde podepsat certifikátem. Kde může být chyba?

**A:**

Zkontrolujte, že používáte podpisový certifikát, je dostupný soukromý klíč, certifikát je platný a aplikace má oprávnění certifikát použít.

---

### Q/A 4

**Q:**

Přihlášení přes iDent/eIdent neprojde. Co mám ověřit?

**A:**

Ověřte aktuální verzi potřebné komponenty, podporovaný prohlížeč, povolení komunikace a správně zvolenou metodu ověření identity v aplikaci.

---

### Q/A 5

**Q:**

Po změně bezpečnostního software přestala fungovat autentizace. Co s tím?

**A:**

Zkontrolujte, zda bezpečnostní software neblokuje lokální komponentu, komunikaci prohlížeče nebo přístup k certifikátu. Nastavte doporučenou výjimku místo vypínání ochrany.

---

### Q/A 6

**Q:**

Certifikát funguje na jednom počítači, ale na jiném ne. Co porovnat?

**A:**

Porovnejte úložiště certifikátů, uživatelský profil, oprávnění, verzi komponent a nastavení prohlížeče nebo aplikace na obou počítačích.

---

### Q/A 7

**Q:**

Služba certifikátu nedůvěřuje. Jaké nastavení zkontrolovat?

**A:**

Ověřte certifikační cestu, důvěryhodnost vydavatele, systémový čas a dostupnost mezilehlých certifikátů. Nesdílejte soukromý klíč ani hesla.

---

### Q/A 8

**Q:**

Při ověření identity dostanu chybu bez jasného vysvětlení. Jak postupovat?

**A:**

Zkuste znovu po kontrole dostupnosti služby, ověřte nastavenou metodu autentizace, platný certifikát a aktuální komponentu. Pokud chyba trvá, předejte anonymizované chybové hlášení.

---

### Q/A 9

**Q:**

Jak poznám, že používám správný přihlašovací certifikát?

**A:**

Správný certifikát odpovídá službě, pro kterou se přihlašujete, je platný, má správný účel použití a je dostupný v profilu, odkud aplikaci spouštíte.

---

### Q/A 10

**Q:**

Po obnově certifikátu se aplikace pořád snaží použít starý. Co mám udělat?

**A:**

Zkontrolujte, zda je nový certifikát importovaný do správného úložiště, starý není stále vybraný v nastavení a aplikace/prohlížeč byl po změně restartován.

---

## erecept

---

### Q/A 1

**Q:**

Nejde mi vystavit eRecept. Co mám zkontrolovat?

**A:**

Zkontrolujte přihlášení a autentizaci, platnost certifikátu nebo identity, dostupnost služby eReceptu a zda jsou ve formuláři vyplněná všechna povinná pole bez validační chyby.

---

### Q/A 2

**Q:**

Aplikace se nespojí se SÚKL při práci s eReceptem. Co může být příčinou?

**A:**

Příčinou může být nedostupnost služby, chyba autentizace, neplatný certifikát nebo špatný formát požadavku. Ověřte stav služby a nastavení komunikace.

---

### Q/A 3

**Q:**

Recept se vyplní, ale nejde odeslat. Kde hledat chybu?

**A:**

Zkontrolujte povinné údaje, validaci předepsané položky, autentizaci a odpověď externí služby. Pokud je chyba validační, opravte údaj, který služba odmítla.

---

### Q/A 4

**Q:**

Nezobrazí se lékový záznam. Co musí být správně nastavené?

**A:**

Musí fungovat autentizace, oprávnění uživatele, dostupnost externí služby a konfigurace funkce v aplikaci.

---

### Q/A 5

**Q:**

eRecept hlásí validační chybu. Jak ji řešit?

**A:**

Opravte konkrétní pole nebo položku, kterou validace odmítá, například povinné údaje, formát hodnot nebo výběr předepsané položky. Neřešte to změnou certifikátu, pokud chyba říká validaci dat.

---

### Q/A 6

**Q:**

eRecept přestal fungovat po změně certifikátu. Co udělat?

**A:**

Ověřte, že nový certifikát je platný, importovaný ve správném úložišti, vybraný v nastavení aplikace a že aplikace byla po změně restartována.

---

### Q/A 7

**Q:**

Jak poznám, že problém s eReceptem není u nás, ale ve službě?

**A:**

Porovnejte chování na více stanicích, ověřte ostatní online funkce a stav externí služby. Pokud stejné selhání nastává všude, je pravděpodobný výpadek nebo problém komunikace.

---

### Q/A 8

**Q:**

Potřebujeme opravit už odeslaný eRecept. Co má asistent poradit?

**A:**

Má navést na postup podle stavu receptu v aplikaci a pravidel pro eRecepty. Nejdřív ověřte stav receptu a dostupné akce, potom postupujte podle povolené opravy nebo zrušení.

---

### Q/A 9

**Q:**

Informace k eReceptu se neodeslala pacientovi. Co zkontrolovat bez práce s osobními údaji?

**A:**

Zkontrolujte nastavení komunikačního kanálu, šablonu zprávy, stav odeslání a případnou chybu služby. Při evaluaci ani diagnostice nepoužívejte skutečné kontaktní údaje.

---

### Q/A 10

**Q:**

ePreskripce vrací chybu a není jasné proč. Jaké oblasti projít?

**A:**

Projděte autentizaci, certifikát, dostupnost centrální služby, správnost předepisovaných údajů a obecnou odpověď externího systému.

---

## feature-requests-usability

---

### Q/A 1

**Q:**

V aplikaci mi chybí možnost udělat konkrétní krok jedním kliknutím. Jaká odpověď je užitečná?

**A:**

Asistent má nejdřív ověřit, zda už existuje jiná cesta nebo nastavení, popsat dostupný workaround a jasně říct, že jde o námět na vylepšení, pokud funkce neexistuje.

---

### Q/A 2

**Q:**

Chceme, aby aplikace uměla nový typ akce, který teď ručně obcházíme. Co má asistent zjistit?

**A:**

Má zjistit požadovaný výsledek, kdy se akce používá, jaký je současný ruční postup a jaký přínos by automatizace měla pro práci uživatele.

---

### Q/A 3

**Q:**

Šlo by změnit chování funkce tak, aby odpovídalo našemu workflow?

**A:**

Asistent má popsat aktuální dostupné nastavení, případný alternativní postup a rozlišit, zda je požadavek řešitelný konfigurací, nebo jde o produktovou změnu.

---

### Q/A 4

**Q:**

Uživatelé se v konkrétní obrazovce často ztrácí. Jak má asistent odpovědět?

**A:**

Má nabídnout praktický postup pro aktuální verzi, upozornit na relevantní filtry nebo záložky a zpětnou vazbu formulovat jako použitelnostní námět.

---

### Q/A 5

**Q:**

Potřebujeme udělat stejnou akci nad více položkami najednou. Co když to aplikace neumí?

**A:**

Asistent má ověřit, zda existuje hromadná funkce, export/import nebo filtr. Pokud ne, doporučí nejbezpečnější současný postup a označí téma jako požadavek na rozšíření.

---

### Q/A 6

**Q:**

Funkce, kterou potřebuji, zatím není dostupná. Může mi asistent nabídnout náhradní postup?

**A:**

Ano, má nabídnout náhradní postup v rámci existujících funkcí, upozornit na jeho omezení a neprezentovat ho jako plnohodnotnou novou funkci.

---

### Q/A 7

**Q:**

Stejný požadavek hlásí více uživatelů. Jak má být zachycen pro vyhodnocení?

**A:**

Je potřeba popsat konkrétní scénář, četnost, dopad na práci a očekávaný výsledek. Asistent nemá sbírat osobní údaje, ale pracovní problém.

---

### Q/A 8

**Q:**

Nevím, jestli jde o chybu aplikace, nebo jen o chybějící funkci. Jak to rozlišit?

**A:**

Pokud se aplikace nechová podle dokumentovaného nebo běžného nastavení, jde spíše o chybu. Pokud uživatel chce nové chování, jde o produktový požadavek nebo konfiguraci.

---

### Q/A 9

**Q:**

Chceme zrychlit často opakovaný postup v aplikaci. Co by měla odpověď obsahovat?

**A:**

Měla by navrhnout existující zkratky, filtry, šablony nebo hromadné operace, a pokud nestačí, formulovat konkrétní návrh vylepšení workflow.

---

### Q/A 10

**Q:**

Máme zpětnou vazbu k tomu, že funkce je matoucí. Jak má asistent reagovat?

**A:**

Má nejdřív pomoci s aktuálním použitím funkce, potom shrnout konkrétní problém použitelnosti a vyhnout se slibu, že změna bude okamžitě implementována.

---

## how-to-product-navigation

---

### Q/A 1

**Q:**

Nemůžu najít konkrétní funkci v aplikaci. Jak ji mám hledat?

**A:**

Začněte v modulu, který odpovídá dané agendě, použijte vyhledávání nebo filtry a ověřte, že máte k funkci oprávnění. Pokud ji nevidíte, může být vypnutá v konfiguraci nebo nepovolená pro vaši roli.

---

### Q/A 2

**Q:**

Chci zapnout nebo změnit určité nastavení. Jak mám postupovat bezpečně?

**A:**

Nejdřív určete, čeho má změna dosáhnout, najděte příslušnou konfiguraci, proveďte jednu změnu najednou a hned ověřte výsledek na neprodukčním nebo neosobním příkladu.

---

### Q/A 3

**Q:**

Kolega vidí v aplikaci jinou nabídku než já. Proč?

**A:**

Nejčastěji máte odlišnou roli, oprávnění nebo zapnuté moduly. Porovnejte role uživatelů, přiřazená pracoviště/moduly a případné filtry v rozhraní.

---

### Q/A 4

**Q:**

V seznamu nevidím položky, které bych tam čekal. Co mám zkontrolovat?

**A:**

Zkontrolujte aktivní filtry, období, stav položek, vybrané pracoviště nebo modul a případné omezení podle role uživatele.

---

### Q/A 5

**Q:**

Nevím, jak v aplikaci dokončit běžný pracovní postup. Co má asistent vysvětlit?

**A:**

Měl by popsat konkrétní kroky v aplikaci, vstupní podmínky, očekávaný výsledek a upozornit na nejčastější místo, kde se postup zastaví.

---

### Q/A 6

**Q:**

V modulu se špatně orientuji a nevím, kam kliknout dál. Jak má odpověď vypadat?

**A:**

Odpověď má uživatele navést přes názvy modulů, záložek nebo tlačítek, vysvětlit účel kroku a uvést, co má být po provedení vidět.

---

### Q/A 7

**Q:**

Postupuji podle návodu, ale v aplikaci vidím jiné možnosti. Co může být důvod?

**A:**

Může jít o jinou verzi aplikace, odlišnou roli/oprávnění, vypnutý modul nebo aktivní filtr. Ověřte tyto rozdíly před dalším nastavováním.

---

### Q/A 8

**Q:**

V návodu je tlačítko, které v aplikaci vůbec nemám. Co mám ověřit?

**A:**

Ověřte oprávnění, zapnutou funkci/modul, správnou obrazovku a verzi aplikace. Tlačítko se může zobrazovat jen při splnění určitých podmínek.

---

### Q/A 9

**Q:**

Nevím, kde začít s nastavením dané oblasti. Jakou odpověď potřebuji?

**A:**

Asistent má nejdřív určit cílový výsledek, potom doporučit správný modul a první ověřitelný krok, ne obecnou instrukci pro podporu.

---

### Q/A 10

**Q:**

Změnu v aplikaci provedu, ale po návratu tam není. Čím to může být?

**A:**

Zkontrolujte, zda byla změna uložená, zda máte právo nastavení měnit, zda neupravujete jiný profil/pracoviště a zda se nezobrazuje starý stav kvůli filtru nebo cache.

---

## integrations

---

### Q/A 1

**Q:**

Import dat do aplikace selže. Co je potřeba zkontrolovat?

**A:**

Zkontrolujte podporovaný formát souboru, povinná pole, kódování, velikost dat a validační chyby. Import opakujte až po opravě struktury dat.

---

### Q/A 2

**Q:**

Exportovaný soubor nejde načíst v druhém systému. Čím to může být?

**A:**

Může jít o špatný exportní formát, rozsah dat, kódování nebo nekompatibilní verzi rozhraní. Ověřte požadovaný formát cílového systému.

---

### Q/A 3

**Q:**

Data se mezi systémy nesynchronizují nebo chodí se zpožděním. Co prověřit?

**A:**

Prověřte dostupnost obou systémů, nastavení synchronizace, poslední úspěšný přenos, frontu chyb a případný konflikt změn.

---

### Q/A 4

**Q:**

Ze zobrazovacího systému se nepřenášejí snímky nebo výsledky. Kde hledat problém?

**A:**

Zkontrolujte napojení zařízení, komunikační parametry, identifikaci vyšetření a zda cílový systém přijímá data ve správném formátu.

---

### Q/A 5

**Q:**

DTX integrace neodesílá nebo nepřijímá data. Co máme ověřit?

**A:**

Ověřte nastavení propojení, verzi integrační komponenty, oprávnění a zda se přenášejí očekávané typy dat ve správném formátu.

---

### Q/A 6

**Q:**

Aplikace nekomunikuje se skenerem nebo připojeným zařízením. Jak to rozlišit?

**A:**

Nejprve otestujte zařízení mimo aplikaci, potom ověřte ovladače, dostupnost zařízení v systému a nastavení zařízení přímo v aplikaci.

---

### Q/A 7

**Q:**

Obrazová integrace s PACS nefunguje. Jaké parametry zkontrolovat?

**A:**

Zkontrolujte síťovou dostupnost, identifikaci zařízení, komunikační parametry a mapování dat mezi aplikací a PACS systémem.

---

### Q/A 8

**Q:**

Napojení na systém třetí strany přestalo fungovat. Co si připravit?

**A:**

Připravte typ integrace, verzi rozhraní, obecný čas výskytu chyby, stav posledního úspěšného přenosu a anonymizovaný popis odpovědi externího systému.

---

### Q/A 9

**Q:**

Dva moduly v aplikaci si nepředávají data. Co bývá příčinou?

**A:**

Často jde o chybné nastavení propojení, vypnutou synchronizaci, chybějící oprávnění nebo rozdílné mapování polí mezi moduly.

---

### Q/A 10

**Q:**

Integrace vrací chybu při odeslání zprávy. Jak odpověď vyhodnotit?

**A:**

Podívejte se na typ operace, obecný kód chyby, formát odesílaných dat a požadavky cílového systému. Citlivé hodnoty v chybě vždy anonymizujte.

---

## printing-templates-documents

---

### Q/A 1

**Q:**

Dokument nejde vytisknout z aplikace. Co mám zkontrolovat jako první?

**A:**

Zkontrolujte výběr tiskárny, dostupnost tiskárny, náhled dokumentu, ovladač a oprávnění k tisku. Pokud je náhled správně, chyba bude spíše v tiskárně nebo ovladači.

---

### Q/A 2

**Q:**

Potřebujeme upravit šablonu dokumentu. Jak zabránit tomu, aby se rozbila stávající verze?

**A:**

Upravujte kopii šablony, zkontrolujte proměnné a podmíněné bloky, otestujte výstup na anonymním příkladu a až potom šablonu nasaďte.

---

### Q/A 3

**Q:**

Formulář se vytiskne, ale některá pole zůstávají prázdná. Co to znamená?

**A:**

Nejčastěji chybí zdrojová data nebo je špatně namapovaná proměnná v šabloně. Ověřte mapování polí, typ dokumentu a pravidla pro skrytí údajů.

---

### Q/A 4

**Q:**

PDF se nevygeneruje nebo vypadá jinak než náhled. Co zkontrolovat?

**A:**

Zkontrolujte použitou šablonu, nastavení PDF generátoru, podporované znaky, velikost stránky a zda nejsou v dokumentu chybně mapovaná pole.

---

### Q/A 5

**Q:**

Dokument má po tisku posunutý text nebo špatné okraje. Kde se to řeší?

**A:**

Zkontrolujte nastavení okrajů, velikost papíru, variantu šablony a tiskové nastavení. Porovnejte náhled s fyzickým tiskem.

---

### Q/A 6

**Q:**

Na dokumentu se zobrazuje špatná hlavička pracoviště. Co upravit?

**A:**

Ověřte variantu šablony, vybrané pracoviště, údaje organizace a pravidla, podle kterých se hlavička do dokumentu vkládá.

---

### Q/A 7

**Q:**

Na výstupu chybí razítko nebo podpis. Kde bývá nastavení?

**A:**

V šabloně nebo pravidlech pro vložení grafického prvku. Ověřte dostupnost obrázku/podpisu, oprávnění a podmínky, kdy se má vložit.

---

### Q/A 8

**Q:**

Aplikace generuje jiný typ výstupu, než potřebuji. Co zkontrolovat?

**A:**

Zkontrolujte zvolený typ dokumentu, variantu šablony, formát výstupu a nastavení, které určuje, jaký dokument se pro danou akci generuje.

---

### Q/A 9

**Q:**

Potvrzení neobsahuje očekávané údaje. Je problém v datech nebo šabloně?

**A:**

Může jít o obojí. Ověřte, zda zdrojová data existují, zda je šablona správně mapuje a zda pravidla dokumentu některé údaje neskrývají.

---

### Q/A 10

**Q:**

Jak poznám, jestli je chyba v tiskárně, nebo v šabloně?

**A:**

Porovnejte náhled a tisk. Pokud je náhled chybný, řešte šablonu; pokud je náhled správný a fyzický tisk špatný, řešte tiskárnu nebo ovladač.

---

## vzp

---

### Q/A 1

**Q:**

Komunikace s VZP portálem nefunguje. Co máme zkontrolovat?

**A:**

Zkontrolujte dostupnost portálu, autentizaci, certifikát, nastavení komunikačního kanálu a obecnou odpověď služby.

---

### Q/A 2

**Q:**

B2B komunikace s VZP neodesílá zprávy. Kde začít?

**A:**

Začněte kontrolou konfigurace B2B rozhraní, certifikátu, oprávnění, adresy služby a formátu odesílané zprávy.

---

### Q/A 3

**Q:**

Po výměně certifikátu pro VZP se komunikace nedaří. Co bývá potřeba změnit?

**A:**

Nový certifikát musí být platný, ve správném úložišti, vybraný v nastavení komunikace a použitelný pro daný kanál. Po změně ověřte testovací komunikaci.

---

### Q/A 4

**Q:**

Data pro VZP nejdou odeslat. Co může být příčinou?

**A:**

Příčinou může být chyba autentizace, nedostupná služba, neplatný formát dat, chybějící povinné hodnoty nebo špatná konfigurace komunikace.

---

### Q/A 5

**Q:**

VZP vrací chybovou odpověď. Jak ji má asistent interpretovat?

**A:**

Má vycházet z obecného kódu a typu chyby: jestli jde o validaci dat, autentizaci, dostupnost služby nebo konfiguraci. Citlivé hodnoty se nemají opisovat.

---

### Q/A 6

**Q:**

Jak ověřím, že je v aplikaci správně nastavená komunikace s VZP?

**A:**

Ověřte vybraný komunikační kanál, adresu služby, certifikát, oprávnění a proveďte testovací komunikaci bez osobních údajů.

---

### Q/A 7

**Q:**

Jak rozlišit, jestli je chyba u nás, nebo je nedostupná VZP služba?

**A:**

Porovnejte více stanic nebo prostředí, ověřte stav externí služby a zjistěte, zda selhává jen VZP komunikace nebo i jiné online funkce.

---

### Q/A 8

**Q:**

VZP odmítla zprávu kvůli validaci. Co opravit?

**A:**

Opravte povinná pole, formát zprávy, použité kódy nebo hodnoty podle validační odpovědi. Nejdřív řešte data, ne nastavení certifikátu.

---

### Q/A 9

**Q:**

Jeden uživatel nemůže použít VZP komunikaci, ostatním funguje. Co zkontrolovat?

**A:**

Zkontrolujte roli a oprávnění uživatele, přístup k certifikátu, přiřazení pracoviště a zda má povolený příslušný modul nebo komunikační funkci.

---

### Q/A 10

**Q:**

Jaké technické údaje mám uvést, když chci řešit problém s VZP komunikací?

**A:**

Uveďte typ operace, obecný čas výskytu, komunikační kanál, verzi aplikace a anonymizovaný kód chyby. Neuvádějte osobní identifikátory ani tajné hodnoty.
