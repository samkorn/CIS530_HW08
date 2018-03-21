cd ~/Python/CIS530/CIS530_HW08/code
python3 depPath/extractDepPathHyponyms.py --inputwikifile ../data/wikipedia_sentences.txt --outputfile depPath/output/deppath_ext.txt
python3 extractDatasetPredictions.py --extractionsfile depPath/output/deppath_ext.txt --trdata ../data/bless2011/data_lex_train.tsv --valdata ../data/bless2011/data_lex_val.tsv --testdata ../data/bless2011/data_lex_test.tsv --trpredfile depPath/output/deppath_tr.txt --valpredfile depPath/output/deppath_val.txt --testpredfile depPath/output/deppath_test.txt
printf "\nTraining Data Performance:\n"
python3 computePRF.py --goldfile ../data/bless2011/data_lex_train.tsv --predfile depPath/output/deppath_tr.txt
printf "\nValidation Data Performance:\n"
python3 computePRF.py --goldfile ../data/bless2011/data_lex_val.tsv --predfile depPath/output/deppath_val.txt