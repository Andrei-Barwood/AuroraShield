#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="${1:-./p01_lab}"
STATUS=0

pass() { echo "[PASS] $1"; }
warn() { echo "[WARN] $1"; }
fail() { echo "[FAIL] $1"; STATUS=1; }

if [[ "$(id -u)" -eq 0 ]]; then
  fail "No ejecutar como root"
else
  pass "Ejecución sin root"
fi

if [[ ! -d "$LAB_DIR" ]]; then
  fail "No existe laboratorio: $LAB_DIR"
  echo "Resultado final: FAIL"
  exit 1
fi

for d in tmp logs artifacts; do
  if [[ -d "$LAB_DIR/$d" ]]; then
    perm=$(stat -f "%A" "$LAB_DIR/$d")
    if [[ "$perm" =~ ^7[0-5][0-5]$ ]]; then
      pass "Permisos aceptables en $LAB_DIR/$d ($perm)"
    else
      warn "Permisos a revisar en $LAB_DIR/$d ($perm)"
    fi
  else
    warn "Directorio faltante: $LAB_DIR/$d"
  fi
done

if find "$LAB_DIR" -type d -perm -0002 | grep -q .; then
  fail "Hay directorios world-writable en $LAB_DIR"
else
  pass "No hay directorios world-writable"
fi

if [[ -f "$LAB_DIR/.env" ]]; then
  if grep -q '^P01_NETWORK_MODE=isolated$' "$LAB_DIR/.env"; then
    pass "Modo de red aislado declarado en .env"
  else
    warn "No se encontró P01_NETWORK_MODE=isolated en .env"
  fi
else
  warn "No existe $LAB_DIR/.env (usar .env.example como base)"
fi

if [[ $STATUS -eq 0 ]]; then
  echo "Resultado final: PASS"
else
  echo "Resultado final: FAIL"
fi

exit $STATUS
