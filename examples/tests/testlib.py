import finsy as fy


async def read_p4_tables(target: str, *, skip_const: bool = False) -> set[str]:
    "Read all table entries from the P4Runtime switch."
    result: set[str] = set()

    async with fy.Switch(f"sw@{target}", target) as sw:
        with sw.p4info:
            # Wildcard-read does not read default entries.
            async for entry in sw.read(fy.P4TableEntry()):
                assert not entry.is_default_action

                # Skip const table entries upon request.
                if skip_const and sw.p4info.tables[entry.table_id].is_const:
                    continue

                if entry.priority != 0:
                    info = f"{entry.table_id} {entry.priority:#x}"
                else:
                    info = entry.table_id

                match_str = entry.match_str(wildcard="*")
                if match_str:
                    result.add(f"{info} {match_str} {entry.action_str()}")
                else:
                    # Table has no match fields.
                    result.add(f"{info} {entry.action_str()}")

            # Read default entries for each table.
            for table in sw.p4info.tables:
                # Skip const table entries upon request.
                if skip_const and table.is_const:
                    continue

                async for entry in sw.read(
                    fy.P4TableEntry(
                        table_id=table.alias,
                        is_default_action=True,
                    )
                ):
                    assert entry.is_default_action
                    assert entry.priority == 0
                    assert entry.match_str() == ""
                    result.add(f"{entry.table_id} {entry.action_str()}")

    return result
