# 基本設定
BASE=http://localhost:8000
AUTH=guest1:guest1password

# 1) 開始新遊戲（取得 session_id / nonce / sig）
START_JSON=$(curl -s -u "$AUTH" -X POST $BASE/api/session/start/)
echo "$START_JSON" | jq .
SESSION_ID=$(echo "$START_JSON" | jq -r .session_id)
NONCE=$(echo "$START_JSON" | jq -r .start_nonce)
SIG=$(echo "$START_JSON" | jq -r .sig)
echo "SESSION_ID=$SESSION_ID  NONCE=$NONCE  SIG=$SIG"

# 2) 送 8 關結果（示範資料）
for i in {1..8}; do
  GRID=$((2+i))
  ELAPSED=$((1000 + i*100))
  curl -s -u "$AUTH" -X POST $BASE/api/session/$SESSION_ID/level \
    -H "Content-Type: application/json" \
    -d "{\"level_index\":$i,\"grid_size\":$GRID,\"elapsed_ms\":$ELAPSED,\"correct\":true}"
  echo
done

# 3) 結束遊戲（帶上 start_nonce / sig，且務必帶 -u）
TOTAL=$((8*1000))
curl -s -u "$AUTH" -X POST $BASE/api/session/$SESSION_ID/finish \
  -H "Content-Type: application/json" \
  -d "{\"total_ms\":$TOTAL,\"start_nonce\":\"$NONCE\",\"sig\":\"$SIG\"}"
echo

# 4) 查排行榜（應該會看到 guest1）
curl -s $BASE/api/leaderboard/?limit=10 | jq .