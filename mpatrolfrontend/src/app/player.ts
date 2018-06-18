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

export class Player {
	id: number;
	character_name: string;
	gold: number;
	xp: number;
	calc: Calc;
	ll: LeaderLevel;
}

export class PlayerUpgradeLeaderLevel {
	id: number;
	current_ll: LeaderLevel;
	next_ll: LeaderLevel;
	all_ll: LeaderLevel[];
	xp: number;
	upgrade_id: number;
}