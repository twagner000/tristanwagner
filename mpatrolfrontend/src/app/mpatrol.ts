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
    cost_xp: number;
    prereq: Technology[];
}

export class Structure {
    id: number;
	name: string;
    cost_gold: number;
    cost_xp: number;
    tech_req: Technology;
    struct_req: Structure;
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