name="no_name_was_input";
while getopts n: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
    esac
done

mkdir runs/${name}
cd runs/${name}
cp ../../generate_run_files.py generate_run_files.py
python3 generate_run_files.py
# rm generate_run_files.py




