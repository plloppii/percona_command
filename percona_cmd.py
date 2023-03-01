
import argparse


column_to_cmd = {
    "id" : "alter table $LAPI_TABLE modify id bigint unsigned not null auto_increment primary key;\n",
    "schedule_id" : "alter table $LAPI_TABLE modify schedule_id bigint unsigned",
    "DEFAULT" : "alter table $LAPI_TABLE modify $DEFAULT bigint unsigned"
}

col_to_percona = {
    "id": "modify id bigint unsigned not null auto_increment primary key, ",
    "schedule_id": "modify schedule_id bigint unsigned",
    "DEFAULT": "modify $DEFAULT bigint unsigned"
}

def create_percona_cmd(table, columns_to_bigint):
    template_file = 'percona_cmd.tmpl'
    with open(template_file, 'r') as file, open("output_cmd", "a") as output:
        lines = file.read()

        migration_lines = ""
        percona_lines = ""
        for c in columns_to_bigint: 
            col = c.split("|")[0].strip()
            is_null = c.split("|")[1:]

            if col in column_to_cmd: 
                migration_lines += column_to_cmd[col]
                percona_lines += col_to_percona[col]
            else: 
                migration_lines += column_to_cmd["DEFAULT"].replace("$DEFAULT", col)
                percona_lines += col_to_percona["DEFAULT"].replace("$DEFAULT", col)
            
            # Null support
            if col == "id": continue
            if is_null: 
                migration_lines += " null;\n"
                percona_lines += " null, "
            else:
                migration_lines += " not null;\n"
                percona_lines += " not null, "

        migration_lines = migration_lines.rstrip("\n")
        percona_lines = percona_lines.rstrip(", ")

        lines = lines.replace("$MIGRATIONS", migration_lines)
        lines = lines.replace("$PERCONA_ALTER", percona_lines)
        lines = lines.replace("$LAPI_TABLE", table.strip())
        output.write(lines)

# create_percona_cmd(table_name)

with open('all_tables') as file:
    for line in file:
        column = line.split(" ")[0]
        columns_to_bigint = line.split(" ")[1:]
        create_percona_cmd(column, columns_to_bigint)