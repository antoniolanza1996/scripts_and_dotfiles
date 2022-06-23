#!/opt/anaconda3/envs/covid_stats/bin/python3
import argparse
import locale
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
import folium
import webbrowser

parser = argparse.ArgumentParser(
    description='Show daily Italian Covid-19 data',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    '-v', '--verbose',
    help='Show more columns and also visualize them on map',
    action='store_true'
)
args = parser.parse_args()

# Change locale with italian:
# it allows to see month written in italian and not in english
locale.setlocale(locale.LC_TIME, 'it_IT')

# Read latest CSV data
url_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv'
df_regioni = pd.read_csv(url_regioni)

# Extract date of pubblication of this data
last_update_data_str = df_regioni['data'].unique()[0]
last_update_data = pd.to_datetime(last_update_data_str).date()

# Remove useless columns and rename three columns (i.e. denominazione_regione, nuovi_positivi e totale_positivi)
columns_to_remove = [
    'data',
    'stato',
    'codice_regione',
    'totale_ospedalizzati',
    'variazione_totale_positivi',
    'dimessi_guariti',
    'casi_da_sospetto_diagnostico',
    'casi_da_screening',
    'tamponi',
    'casi_testati',
    'note',
]
df_regioni.drop(columns_to_remove, axis=1, inplace=True)
df_regioni.rename(columns={
    'denominazione_regione': 'Regione',
    'nuovi_positivi': 'nuovi_positivi_odierni',
    'totale_positivi': 'attualmente_positivi'
    }, inplace=True)

# verbose or not?
if not args.verbose:
    # Prepare DataFrame to be printed on terminal
    df_minimal = df_regioni[
        ['Regione', 'nuovi_positivi_odierni', 'attualmente_positivi']
    ]
    df_to_show = df_minimal
else:
    # Prepare DataFrame to be printed on terminal
    df_to_show = df_regioni

    # Map creation with folium (and visualization on the browser)
    folium_map = folium.Map(
        location=[41.8719, 12.5674],
        tiles='OpenStreetMap',
        min_zoom=5,
        max_zoom=10,
        zoom_start=6,
    )
    RADIUS_MULT = 50
    for i in range(0, len(df_regioni)):
        folium.Circle(
            location=[df_regioni.iloc[i]["lat"], df_regioni.iloc[i]["long"]],
            color="crimson",
            fill=True,
            fill_color="crimson",
            tooltip="<li><bold>Regione: "
            + str(df_regioni.iloc[i]["Regione"])
            + "<li><bold>Nuovi positivi odierni: "
            + str(df_regioni.iloc[i]["nuovi_positivi_odierni"])
            + "<li><bold>Attualmente positivi: "
            + str(df_regioni.iloc[i]["attualmente_positivi"])
            + "<li><bold>Isolamento domiciliare: "
            + str(df_regioni.iloc[i]["isolamento_domiciliare"])
            + "<li><bold>Ricoverati con sintomi: "
            + str(df_regioni.iloc[i]["ricoverati_con_sintomi"])
            + "<li><bold>Terapia intensiva: "
            + str(df_regioni.iloc[i]["terapia_intensiva"]),
            radius=int(df_regioni.iloc[i]["nuovi_positivi_odierni"]) * RADIUS_MULT,
        ).add_to(folium_map)

    url = '/tmp/map.html'
    folium_map.save(outfile=url)
    webbrowser.open(f"file://{url}", new=1)

# Print to stdout
# NB: 'today' e 'yesterday' si riferiscono rispettivamente all'ultimo giorno
# in cui si possiedono dei dati e il giorno precedente. Quindi se si esegue questo script
# dopo le 18:00 (i.e. solito orario in cui il Dipartimento della Protezione Civile aggiorna i dati),
# effettivamente today==giorno corrente. Altrimenti today==giorno precedente perché per il
# giorno corrente non sono stati ancora pubblicati i dati. Tuttavia, in output viene segnalato
# tutto correttamente in funzione dei dati a disposizione.

PRINT_SEP = f"{'+'*73}\n{'+'*73}"
print(f"{PRINT_SEP}\n{'+'*21} Dati regionali del {last_update_data.strftime('%d %B')} {'+'*21}\n{PRINT_SEP}")
print(tabulate(df_to_show, headers='keys', tablefmt='pretty', showindex='never'))
print(PRINT_SEP)
nuovi_positivi_today = df_to_show['nuovi_positivi_odierni'].sum()
print(f"Numero di nuovi casi positivi in Italia il {last_update_data.strftime('%d %B')} = {nuovi_positivi_today}")

url_regioni_today = f"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{last_update_data.strftime('%Y%m%d')}.csv"
df_regioni_today = pd.read_csv(url_regioni_today)  # NB: qui potrei usare
# anche direttamente df_regioni in quanto il 'latest' coincide con il
# 'last_update_data' ma ricarico per sicurezza il CSV perché se si usa
# l'opzione NON verbose, la colonna 'tamponi' viene eliminata

yesterday = last_update_data + timedelta(days=-1)
url_regioni_yesterday = f"https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{yesterday.strftime('%Y%m%d')}.csv"
df_regioni_yesterday = pd.read_csv(url_regioni_yesterday)

num_tamponi_done_today = (
    df_regioni_today['tamponi'].sum() - df_regioni_yesterday['tamponi'].sum()
)
print(f"Numero di tamponi effettuati in Italia il {last_update_data.strftime('%d %B')} = {num_tamponi_done_today}")

percentual = round((nuovi_positivi_today / num_tamponi_done_today) * 100, 2)
print(f"Rapporto positivi/tamponi il {last_update_data.strftime('%d %B')} = {percentual}%")

today_date = datetime.now().date()
if last_update_data != today_date:
    print(PRINT_SEP)
    print(f"[!] Attenzione: i dati non sono ancora aggiornati alla data odierna (i.e. {today_date.strftime('%d %B')})!")
print(PRINT_SEP)
