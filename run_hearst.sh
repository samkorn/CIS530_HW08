cd ~/Python/CIS530/CIS530_HW08/code
python3 hearst/extractHearstHyponyms.py --inputwikifile ../data/wikipedia_sentences.txt --outputfile hearst/output/hearst_ext.txt
python3 extractDatasetPredictions.py --extractionsfile hearst/output/hearst_ext.txt --trdata ../data/bless2011/data_lex_train.tsv --valdata ../data/bless2011/data_lex_val.tsv --testdata ../data/bless2011/data_lex_test.tsv --trpredfile hearst/output/hearst_tr.txt --valpredfile hearst/output/hearst_val.txt --testpredfile hearst/output/hearst_test.txt
printf "\nTraining Data Performance:\n"
python3 computePRF.py --goldfile ../data/bless2011/data_lex_train.tsv --predfile hearst/output/hearst_tr.txt
printf "\nValidation Data Performance:\n"
python3 computePRF.py --goldfile ../data/bless2011/data_lex_val.tsv --predfile hearst/output/hearst_val.txt