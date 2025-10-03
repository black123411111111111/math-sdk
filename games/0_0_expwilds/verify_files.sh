#!/bin/bash
# Verification script to check all required Stake Engine files exist

echo "==================================="
echo "Premium Dragon Wilds File Verification"
echo "==================================="
echo ""

GAME_DIR="/home/runner/work/math-sdk/math-sdk/games/0_0_expwilds"
LIBRARY_DIR="$GAME_DIR/library"
PASS=0
FAIL=0

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $2 ($(du -h "$1" | cut -f1))"
        ((PASS++))
    else
        echo "❌ $2 - MISSING"
        ((FAIL++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ Directory: $2"
        ((PASS++))
    else
        echo "❌ Directory: $2 - MISSING"
        ((FAIL++))
    fi
}

echo "Checking directories..."
check_dir "$LIBRARY_DIR/publish_files" "publish_files"
check_dir "$LIBRARY_DIR/configs" "configs"
check_dir "$LIBRARY_DIR/forces" "forces"
check_dir "$LIBRARY_DIR/lookup_tables" "lookup_tables"
echo ""

echo "Checking publish files (required for RGS)..."
check_file "$LIBRARY_DIR/publish_files/books_base.jsonl.zst" "books_base.jsonl.zst"
check_file "$LIBRARY_DIR/publish_files/books_bonus.jsonl.zst" "books_bonus.jsonl.zst"
check_file "$LIBRARY_DIR/publish_files/books_superspin.jsonl.zst" "books_superspin.jsonl.zst"
check_file "$LIBRARY_DIR/publish_files/lookUpTable_base_0.csv" "lookUpTable_base_0.csv"
check_file "$LIBRARY_DIR/publish_files/lookUpTable_bonus_0.csv" "lookUpTable_bonus_0.csv"
check_file "$LIBRARY_DIR/publish_files/lookUpTable_superspin_0.csv" "lookUpTable_superspin_0.csv"
check_file "$LIBRARY_DIR/publish_files/index.json" "index.json"
echo ""

echo "Checking config files..."
check_file "$LIBRARY_DIR/configs/config.json" "config.json"
check_file "$LIBRARY_DIR/configs/config_fe_0_0_expwilds.json" "config_fe_0_0_expwilds.json"
check_file "$LIBRARY_DIR/configs/event_config_base.json" "event_config_base.json"
check_file "$LIBRARY_DIR/configs/event_config_bonus.json" "event_config_bonus.json"
check_file "$LIBRARY_DIR/configs/event_config_superspin.json" "event_config_superspin.json"
echo ""

echo "Checking force files..."
check_file "$LIBRARY_DIR/forces/force.json" "force.json"
check_file "$LIBRARY_DIR/forces/force_record_base.json" "force_record_base.json"
check_file "$LIBRARY_DIR/forces/force_record_bonus.json" "force_record_bonus.json"
check_file "$LIBRARY_DIR/forces/force_record_superspin.json" "force_record_superspin.json"
echo ""

echo "==================================="
echo "Verification Summary"
echo "==================================="
echo "✅ Passed: $PASS"
echo "❌ Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 All required files are present!"
    echo "The game is ready for Stake Engine upload."
    echo ""
    echo "Total package size:"
    du -sh "$LIBRARY_DIR/publish_files"
    du -sh "$LIBRARY_DIR/configs"
    du -sh "$LIBRARY_DIR/forces"
    exit 0
else
    echo "⚠️  Some files are missing. Please run simulations."
    exit 1
fi
