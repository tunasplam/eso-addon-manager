# fix our upload problem. Replace broken .lua files with correct empty tables.

# Dir with our tables
current_dir=~/LinkESOAddons/SavedVariables
# Dir with empty file lua table
empty_file=~/LinkESOAddons/HarvestMap/Main/emptyTable.lua

for zone in AD EP DC DLC NF; do
	fn=HarvestMap${zone}.lua
	echo "${fn}..."
	file_dir=${current_dir}/${fn}

	# clear file by entering name
	echo -n Harvest${zone}_SavedVars > "${file_dir}"
	# append lua table
	cat "${empty_file}" >> "${file_dir}"
	#echo -n Harvest${zone}_SavedVars | cat "${empty_file}" > "${file_dir}"
done
