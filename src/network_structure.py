def build_network_structure(num_groups, prosumers_per_group, consumers_per_group):
    assert len(prosumers_per_group) == num_groups
    assert len(consumers_per_group) == num_groups
    groups = {}
    for g in range(num_groups):
        group_id = g + 1
        groups[group_id] = []
        local_uid = 1
        for _ in range(prosumers_per_group[g]):
            house_id = f"g{group_id}h{local_uid}"
            groups[group_id].append({
                "id": house_id,
                "uid": local_uid,
                "group": group_id,
                "type": "prosumer"
            })
            local_uid += 1
        for _ in range(consumers_per_group[g]):
            house_id = f"g{group_id}h{local_uid}"
            groups[group_id].append({
                "id": house_id,
                "uid": local_uid,
                "group": group_id,
                "type": "consumer"
            })
            local_uid += 1
    return groups





