export MODEL_FILE=model.json
ask api update-model -s $SKILL_ID -l en-US -f $MODEL_FILE
ask api update-model -s $SKILL_ID -l en-GB -f $MODEL_FILE
ask api update-model -s $SKILL_ID -l en-CA -f $MODEL_FILE
ask api update-model -s $SKILL_ID -l en-IN -f $MODEL_FILE
ask api update-model -s $SKILL_ID -l de-DE -f $MODEL_FILE
ask api update-model -s $SKILL_ID -l ja-JP -f $MODEL_FILE