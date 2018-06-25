export class Calc {
	cp_avail: number;
}

export class BriefCreature {
	id: number;
	name: string;
	cost_cp: number;
	cost_gold: number;
}

export class Creature extends BriefCreature {
	plural_name: string;
    min_ll: number;
    attack: number;
    defense: number;
    work_gold: number;
    work_xp: number;
    oversee: number;
}

export class BriefLeaderLevel {
	id: number;
	level: number;
	cost_xp: number;
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

export class Technology extends BriefTechnology {
    min_ll: number;
    prereq: Technology[];
}

export class BriefStructure {
    id: number;
	name: string;
    cost_gold: number;
    cost_xp: number;
}

export class Structure extends BriefStructure{
    id: number;
	name: string;
    cost_gold: number;
    cost_xp: number;
}

export class BriefWeaponBase {
	id: number;
	name: string;
	cost_gold: number;
}

export class BriefWeaponMaterial {
	id: number;
	name: string;
	cost_mult: number;
}

export class Battalion {
	id: number;
	battalion_number: number;
	creature: BriefCreature;
	count: number;
	level: number;
	weapon_base: BriefWeaponBase;
	weapon_material: BriefWeaponMaterial;
	up_opts_creature: BriefCreature[];
}

export class Player {
	id: number;
	character_name: string;
	ll: LeaderLevel;
	gold: number;
	xp: number;
	technologies: Technology[];
	structures: Structure[];
	battalions: Battalion[];
	calc: Calc;
	up_opt_ll: BriefLeaderLevel;
	up_opts_structure: BriefStructure[];
	up_opts_technology: BriefTechnology[];
}