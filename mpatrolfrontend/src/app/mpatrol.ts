export class Calc {
	avail_xp: number;
}

export class Creature {
  id: number;
  name: string;
}

export class BriefLeaderLevel {
	id: number;
	level: number;
	xp_cost: number;
}

export class LeaderLevel extends BriefLeaderLevel {
	life: number;
	cp: number;
}

export class BriefTechnology {
    id: number;
	name: string;
    cost_xp: number;
}

export class Technology {
    id: number;
	name: string;
    cost_xp: number;
    min_ll: number;
    prereq: Technology[];
}

export class BriefStructure {
    id: number;
	name: string;
    cost_gold: number;
    cost_xp: number;
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
	up_opt_ll: BriefLeaderLevel;
	up_opts_structure: BriefStructure[];
	up_opts_technology: BriefTechnology[];
}