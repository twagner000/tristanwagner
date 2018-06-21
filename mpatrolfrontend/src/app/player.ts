export class Calc {
	avail_xp: number;
}

export class LeaderLevel {
	id: number;
	level: number;
	life: number;
	cp: number;
	xp_cost: number;
}

export class Technology {
    id: number;
	name: string;
    level: number;
    cost: number;
    prereq: Technology[];
}

export class Structure {
    id: number;
	name: string;
    cost_gold: number;
    cost_xp: number;
    tech_req: Technology[];
    struct_req: Structure[];
    effects: string;
}

export class Player {
	id: number;
	character_name: string;
	ll: LeaderLevel;
	gold: number;
	xp: number;
	technologies: Technology[];
	structures: Structure[];
	calc: Calc;
	ll_upgrade: LeaderLevel;
	structure_upgrade: Structure[];
	technology_upgrade: Technology[];
}

export class PlayerUpgradeLeaderLevel {
	id: number;
	current_ll: LeaderLevel;
	next_ll: LeaderLevel;
	all_ll: LeaderLevel[];
	xp: number;
	upgrade_id: number;
}

export class PlayerUpgrade {
	player_id: number;
	upgrade_type: string;
	upgrade_id: number;
}