#!/usr/bin/env bash
set -euo pipefail
cd /data

PROFILE="/opt/car.lua"   # default: /opt/car.lua
ALGORITHM="mld"          # default: mld
# ----------------------------------------------------------------------

# Localiza o único .osm.pbf da pasta (usado no processamento)
find_pbf() {
  shopt -s nullglob; local f=( *.osm.pbf ); shopt -u nullglob
  if [ "${#f[@]}" -ne 1 ]; then
    echo "ERRO: esperado exatamente um arquivo .osm.pbf na pasta de dados (encontrados: ${#f[@]})." >&2
    echo "Baixe um extrato em https://download.geofabrik.de/ e deixe apenas ele na pasta." >&2
    exit 1
  fi
  printf '%s\n' "${f[0]}"
}

# Localiza os dados já processados (usado ao servir)
find_osrm() {
  shopt -s nullglob; local f=( *.osrm.fileIndex ); shopt -u nullglob
  if [ "${#f[@]}" -ne 1 ]; then
    echo "ERRO: dados processados não encontrados (esperado um *.osrm.fileIndex)." >&2
    echo "Rode primeiro: docker compose run --rm processor" >&2
    exit 1
  fi
  printf '%s\n' "${f[0]%.fileIndex}"
}

case "${1:-}" in
  process)
    PBF="$(find_pbf)"
    OSRM="${PBF%.osm.pbf}.osrm"
    echo "==> [1/3] osrm-extract: ${PBF} (perfil ${PROFILE})"
    osrm-extract -p "${PROFILE}" "${PBF}"
    if [ "${ALGORITHM}" = "ch" ]; then
      echo "==> [2/3] osrm-contract (algoritmo CH)"
      osrm-contract "${OSRM}"
      echo "==> [3/3] CH não requer customize."
    else
      echo "==> [2/3] osrm-partition (algoritmo MLD)"
      osrm-partition "${OSRM}"
      echo "==> [3/3] osrm-customize"
      osrm-customize "${OSRM}"
    fi
    echo "==> Processamento concluído."
    ;;
  serve)
    OSRM="$(find_osrm)"
    echo "==> Servindo dados processados (algoritmo ${ALGORITHM})"
    exec osrm-routed --algorithm "${ALGORITHM}" \
      --max-table-size "${OSRM_MAX_TABLE_SIZE:-2000}" \
      --max-trip-size "${OSRM_MAX_TRIP_SIZE:-2000}" \
      "${OSRM}"
    ;;
  *)
    echo "Uso: entrypoint.sh [process|serve]" >&2
    exit 1
    ;;
esac
