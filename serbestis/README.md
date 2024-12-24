VTISearch - VirusTotal Kəşfiyyat Axtarışı
VTISearch VirusTotal Kəşfiyyat axtarış sorğusunu işlətmək üçün kiçik bir utilitdir. Sorğu, sənədləşmədə verilən güclü axtarış modifikatorlarını əhatə edə bilər ki, bu da təhdid araşdırması və ovçuluq əməliyyatlarını effektiv şəkildə həyata keçirməyə imkan verir.

Proqram VirusTotal API-nin v3 versiyasından istifadə edir. Xahiş edirik nəzərə alın ki, Kəşfiyyat Axtarışı (və proqramın digər funksiyalarının çoxu) üçün özəl API açarına ehtiyacınız var, yəni VirusTotal Enterprise xidmətinə girişiniz olmalıdır. API açarı ilk başladıqda tələb olunur və təhlükəsizlik səbəbi ilə sistemin açar saxlamağına (keyring) saxlanılır.

Əvvəlcədən olaraq, VTISearch axtarış sorğusuna bağlı ilk 20 nümunə haqqında məlumat alır. Lakin -l (--limit) parametri ilə 300 nümunəyə qədər nəticələr tələb oluna bilər.

Məlumatlar nümunə şifrələrini (MD5, SHA1, SHA256 və varsa VirusTotal vhash oxşarlıq şifrəsi), artefaktın növü və ölçüsünü, təqdimat tarixlərini (ilk və sonuncu) və həmçinin aşkarlama statistikalarını əhatə edir.

Əlavə detalları, məsələn, hər bir tədqiqatçı tərəfindən skan edilmiş nəticələri göstərmək üçün -v (verbose) parametri istifadə edilə bilər. Üç fərqli məlumat dərəcəsi dəstəklənir.

VTISearch həmçinin əlaqəli nümunələri və davranış (dinamik analiz) hesabatlarını yükləməyə imkan verir. Dinamik analiz hesabatları avtomatik olaraq şəbəkə əsaslı Kompromis Göstəriciləri (IOC) çıxarmaq üçün təhlil edilir.

--csv seçimi istifadə edildikdə, nəticələr CSV formatında ixrac edilə bilər və sonradan Maltego və ya digər qraf vizuallaşdırma proqramlarına idxal edilə bilər.

Xüsusiyyətlər
Axtarış sorğusuna bağlı olan 300-ə qədər artefaktın (nümunə, domen, URL) məlumatlarını əldə edir.
Məlumatlar meta məlumatları ilə yanaşı, tələb olunduqda ətraflı skanerləmə və aşkarlama nəticələrini də əhatə edir.
Əlaqəli nümunələri və davranış (dinamik analiz) hesabatlarını avtomatik olaraq yükləyir.
Davranış hesabatları avtomatik olaraq şəbəkə əsaslı Kompromis Göstəriciləri (IOC) üçün skan edilir.
Əməliyyatları sürətləndirmək üçün çoxlu işçilərdən istifadə edir.
Bütün məlumatlar müxtəlif alt qovluqlarda kateqoriyalara ayrılır. Ətraflı qeydlər sonrakı işləmələr üçün faydalıdır.
Nəticələr CSV formatında ixrac edilə bilər və sonra əlaqələrin vizuallaşdırılması üçün, məsələn, Maltego proqramına idxal edilə bilər.


## Requirements and Installation

* Linux operating system (tested on Ubuntu 18.04)

* Python 3.7+
* pip3
* vt-py
* keyring

### Notes on Python 3.7 and Ubuntu 18.04

1. By default, Python 3.6 is still installed on Ubuntu 18.04. You can install version 3.7 (or 3.8) with

```bash
$ sudo apt-get install python3.7
```

and then change to the new version with\*

```
$ sudo update-alternatives --config python3
```

(\* In case you should get an error message that no alternative had been found, please run `sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1`.)

If you subsequently run `python3 --version` you should see the new version. Please note that you might have to reinstall respective packages for this version.


2. Please reinstall pip3 with

```
$ sudo apt-get install --reinstall python3-pip
```


### Package installation and Repository Cloning

1. Once Python 3.7 is avaialble, you can comfortably install all required packages as follows:

```bash
$ sudo pip3 install vt-py keyring 
```

(I am globally installing the packages in this example. Please feel free to set up a virtual environment instead if you prefer.)


2. Clone the *VTISearch* repository, and start the program:

```
$ git clone https://github.com/svo80/vti_search.git .

$ cd vti_search && python3 vti_search -h
```


## Options and Usage

```
usage: vti_search.py [-h] [-q QUERY] [-l LIMIT] [--logfile LOG]
                     [--download-dir DOWNLOAD_DIR] [-d] [-f SAMPLE_FILE]
                     [--no-behavior] [-v] [--csv]

optional arguments:
  -h, --help                          Show this help message and exit

  -q QUERY, --query QUERY             Run a VirusTotal Intelligence search query.

  -l LIMIT, --limit LIMIT             Limits the number of samples to return.

  --logfile LOG                       Name of the log file.

  --download-dir DOWNLOAD_DIR         Name of the directory where retrieved information will
                                      be stored in.

  -d, --download                      If set, also downloads samples from VirusTotal that
                                      are referenced in an Intelligence search.

  -f SAMPLE_FILE, --file SAMPLE_FILE  Downloads samples that are referenced in a file.

  --no-behavior                       If set, does not download behavior reports for
                                      samples.

  -v, --verbose                       If set, display verbose information about reports. Use
                                      -vvv to see detailed scan results.

  -u, --update-key                    If set, offers to enter a new API key.

  -w, --workers WORKERS               Number of concurrent workers.

  --csv                               If set, display results as comma-separated values.
```

Əksər hallarda, VTISearch -q (--query) parametri ilə işlədiləcəkdir. Bu sorğu VirusTotal-ə v3 API vasitəsilə göndərilir. Əlaqəli nümunələr əvvəlcədən yüklənməyəcəkdir. Lakin bu prosedur -d parametri ilə asanlıqla aktivləşdirilə bilər.

```bash
$ python3 vti_search.py -q "evil.exe" -d
```

Kəşfiyyat axtarışı yerinə, həmçinin bir faylda saxlanılan şifrələrin siyahısını işləmək mümkündür. Beləliklə, proqram sürətli nümunə yükləyicisi və IOC işləyicisi kimi istifadə oluna bilər:

```bash
$ python3 python3 vti_search.py -f ./iocs.txt
```

Yanaşmalar həmçinin qarışdırıla bilər. Məsələn, əvvəlcə bir sorğunun nəticələrini bir az daha ətraflı yoxlamaq, hədəf nümunələrinin siyahısını uyğunlaşdırmaq və sonra proqramı yenilənmiş nümunə siyahısı üçün yükləmə seçimi aktivləşdirərək yenidən işlətmək istəyə bilərsiniz.

Alternativ olaraq, Kəşfiyyat axtarışının nəticələrini (üçüncü tərəf) hesabatında işarələnmiş göstəricilər ilə birləşdirərək, spesifik bir kampaniya və ya əməliyyat haqqında daha ətraflı bir ümumi baxış yaratmaq istəyə bilərsiniz.

Əvvəlcədən təyin edilmiş olaraq, bütün jurnal faylları, nümunələr və hesabatlar proqram başladıqda downloads qovluğunda yaradılan ayrıca bir qovluqda (zaman damgası ilə tanınan) saxlanılır. Əgər mövcud bir qovluğu yeniləmək istəyirsinizsə, --download-dir parametrini açıq şəkildə təyin edə bilərsiniz.

Məsələn, əgər bir APT kampaniyasını araşdırmaq istəyirsinizsə, Kəşfiyyat axtarışı edə, ilk 100 nəticəni ətraflı formatda əldə edə və bütün məlumatları xüsusi bir qovluqda saxlaya bilərsiniz:

```bash
$ python3 vt_search.py -d -q <query> -l 100 -vvv --download-dir=downloads/apt
```

Nümunə Axtarışlar və Kəşfiyyat Axtarışları
Aşağıdakı axtarışlar yalnız proqramın axtarış imkanlarını və mümkün istifadə halları göstərmək məqsədilə nümayiş məqsədli olaraq verilmişdir:

2020-ci ilin 1 mayından sonra təqdim edilən və beşdən çox, amma on vendor tərəfindən aşkarlanan nümunələri göstərin.
bash
Kodu kopyala
$ python3 vti_search.py -q "ls:2020-05-01+ positives:5+ positives:10-" -v --no-behavior
Alman dilində olan və email əlavəsi olaraq göndərilən, içində JavaScript yerləşdirilmiş PDF sənədlərini göstərin.
ruby
Kodu kopyala
$ python3 vti_search.py -q "tag:attachment type:pdf lang:german tag:js-embedded"
300KB-dən az ölçüsü olan və beşdən çox vendor tərəfindən aşkarlanan imzalanmış icra edilə bilən faylları göstərin.
bash
Kodu kopyala
$ python3 vti_search.py -q "size:300KB- positives:5+ tag:signed type:peexe"
Açıldıqda kodu icra edən və davamlılıq üçün AutoRun açarını qurma ehtimalı olan Microsoft Office sənədlərini (beş nümunəyə qədər) göstərin.
bash
Kodu kopyala
$ python3 vti_search.py -q "behavior:'currentversion\run\' type:docx tag:auto-open" -l 5
Məlumatın İxracı və Əməkdaşlıq
VTISearch bütün məlumatları CSV formatında ixrac etməyi dəstəkləyir. İxrac olunan məzmunlar, məlumat dərəcəsinin səviyyəsindən asılıdır.

Məsələn, -vvv parametrini təyin edərkən, ətraflı antivirus skanerləmə hesabatları CSV formatında ixrac ediləcək. Digər tərəfdən, yalnız -v parametrini təyin edərkən, daha yüksək səviyyəli xülasə statistikaları yaradılacaq.

Dinamik analiz sandbox hesabatlarından əldə olunan şəbəkə göstəricilərinin siyahısı da CSV formatında ixrac edilə bilər. Bu məlumat daha sonra, məsələn, Maltego ilə yüklənərək müvafiq əlaqələrin vizuallaşdırılmasını təmin edə bilər.


## Example Run

```bash
$ python3 vti_search.py -d -q evil.exe -l 10 -vv

VTISearch - VirusTotal Intelligence Search - Version 0.1.0

Written by Stefan Voemel.
------------------------------------------------------------------------------------------

2axxxxxxxxxe4b2be454ed0dxxxxxxxxxx7db18e9780xxxxxxxx10dcabxxxxxx
  MD5:                        xxxxx09dxxxxxc271cxxxxx5cb6xxxxx
  Sha1:                       xxxxxx71bxxxxx4aaxxxx383xxxxce8xxxxe00xx
  VHash:                      xxx04xx5xdxx1xx8xxxx2txxxx

  Type:                       PE32 executable for MS Windows (GUI) Intel 80386 32-bit
  Type Tag:                   peexe
  Size:                       73802

  First submission:           2020-05-07 11:16:58
  Last submission:            2020-05-07 11:16:58
  Number of submissions:      1
  Unique sources:             1

  Malicious:                  58
  Suspicious:                 0
  Undetected:                 14

  [Host]                      1xx.16.xxx.xxx:4444

798xxxx29xxxx4xxxe3dxxxa8xfxx3x2excxxxe7xxc4cxxxd4x4fx4x05xxxxxx
  MD5:                        xxxx27xxxx28xxxx14xxxb34xxx13xxx
  Sha1:                       xxxxb6xxx1f4xxxxdb26xxxx94xxxx5dxx61cxxx
  VHash:                      xxx03xxx7dxxx2xx

  Type:                       PE32 executable for MS Windows (console) Intel 80386 32-bit
  Type Tag:                   peexe
  Size:                       4752

  First submission:           2011-07-04 22:00:08
  Last submission:            2020-05-06 13:39:21
  Number of submissions:      1951
  Unique sources:             1472

  Malicious:                  58
  Suspicious:                 0
  Undetected:                 14

  [Host]                      1xx.1xx.221.22:80
  [Host]                      1xx.1xx.131.241:80
  [Host]                      1xx.xxx.78.24:443
  [Host]                      1xx.xxx.78.25:443
  [URL]                       hxxp://www.xxxxxxxx.com/ad.html
```


## File Structure

```bash
├── downloads                     Program data
│   └── <timestamp>
│       ├── artifacts.txt         List of artifacts that were in scope
│       ├── behavior/             Directory for behavioral reports
│       ├── csv                   Directory with CSV files
│       │   ├── domains.csv       Exported domains (if existing)
│       │   ├── network_iocs.csv  Exported network indicators
│       │   ├── samples.csv       Exported samples (if existing)
│       │   └── urls.csv          Exorted URLs (if existing)
│       ├── log.txt               Detailed log file with program runtime messages
│       ├── reports/              Directory for summary reports and network indicators (*.ioc)
│       │   ├── <sample>          Textual summary report for a sample
│       │   ├── <sample.ioc>      Extracted network indicators for a sample
│       │   ├── <sample.raw>      Static analysis report for a sample in JSON format
│       ├── samples/              Directory for malware samples
│   
├── lib                           Program libraries
│   ├── auxiliary.py
│   ├── sandboxes.py
│   └── vt.py
│   
├── README.md
└── vti_search.py                 Main program file
```



