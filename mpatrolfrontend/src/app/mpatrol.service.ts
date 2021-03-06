import { Injectable, isDevMode } from '@angular/core';
import { Router } from '@angular/router';
import { Player, PublicPlayer, PlayerScore, Battalion, LeaderLevel, Structure, Technology, Creature, WeaponBase, WeaponMaterial, GamePlayer, PlayerLog } from './mpatrol';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

export class PlayerUpgrade {
	constructor(
		public upgrade_type: string,
		public upgrade_id: number
	) { }
}

export class PlayerAction {
    constructor(
		public action: string,
		public target_player_id: number
	) { }
}

export class BattalionUpdate {
	constructor(
		public creature_id: number,
		public count_delta: number,
		public level: number,
		public weapon_base_id: number,
		public weapon_material_id: number
	) { }
}

export class Message {
	constructor(
		public type: string,
		public message: string,
		public debug: boolean
	) { }
}

@Injectable({
	providedIn: 'root'
})

export class MpatrolService {
	private url = '/mpatrol-api/';
	private token = new BehaviorSubject<string>(null);
	private httpOptions = {headers: new HttpHeaders({
		'Content-Type': 'application/json',
		'Authorization': ''
		})};
	private player = new BehaviorSubject<Player>(null);
	private playerLogs = new BehaviorSubject<PlayerLog[]>(null);
	private player_id: number = null;
	private refreshingPlayer: boolean = false;
	messages: Message[] = [];
	private errors = new BehaviorSubject<any>(null);
	private playlist = [];
	private playlist_index = -1;
	audio = new Audio();
	
	constructor(
		private http: HttpClient,
		private router: Router
	) {
		if (isDevMode())
			this.url = 'http://127.0.0.1:8000' + this.url;
		for (var i=1; i<=10; i++)
			this.playlist.push(`/static/mpatrolfrontend/assets/${i}.mp3`);
		this.nextSong(false);
		this.audio.onended = () => this.nextSong();
		this.refreshToken().subscribe(token => {
			if (!token) this.router.navigate(['/']);
		});
	}
	
	getToken() {
		return this.token.asObservable();
	}
	
	refreshToken() {
		(isDevMode() ? this.http.post(`${this.url}auth-token/`, { 'username': 'luke', 'password': 'password' }, this.httpOptions) : this.http.get<Object>(`${this.url}auth-token/`))
			.pipe(
				catchError(this.handleError<any>(`refreshToken`))
			)
			.subscribe(result => {
				let new_token = null;
				if (result && result['token'])
					new_token = result['token'];
				this.httpOptions.headers = this.httpOptions.headers.set('Authorization', `Token ${new_token}`);
				this.token.next(new_token);
			});
		return this.token.asObservable();
	}
	
	nextSong(autoplay: boolean = true) {
		this.playlist_index += 1;
		this.playlist_index %= this.playlist.length;
		this.audio.src = this.playlist[this.playlist_index];
		this.audio.load();
		if (autoplay) this.audio.play();
	}
	
	previousSong(autoplay: boolean = true) {
		this.playlist_index += this.playlist.length-1;
		this.playlist_index %= this.playlist.length;
		this.audio.src = this.playlist[this.playlist_index];
		this.audio.load();
		if (autoplay) this.audio.play();
	}
	
	toggleAudio(): boolean {
		if (this.audio.paused)
			this.audio.play();
		else
			this.audio.pause();
		return this.audio.paused;
	}

	addMessage(type: string, msg: string, debug: boolean = true) {
		this.messages.push(new Message(type,msg,debug));
	}

	clearMessages() {
		this.messages = [];
	}

	getErrors(): Observable<any> {
		return this.errors.asObservable();
	}
	
	setPlayer(player_id: number) {
		this.clearPlayer();
		this.player_id = player_id;
		this.getPlayer();
		this.getPlayerLogs();
	}
	
	joinGame(game_id: number, character_name: string): Observable<any> {
		return this.http.post(`${this.url}game/${game_id}/player/`, {'character_name': character_name}, this.httpOptions)
			.pipe(
				tap(result => {
					this.addMessage('info',`joined game_id=${game_id}`);
				}),
				catchError(this.handleError<any>(`joinGame`))
			);
	}

	getPlayer(): Observable<Player> {
		if (!this.player_id) {
			this.router.navigate(['/choose']);
		} else if (!this.player.getValue() && !this.refreshingPlayer) {
			this.refreshPlayer();
		}
		return this.player.asObservable();
	}
	
	getPlayerLogs (): Observable<PlayerLog[]> {
		return this.playerLogs.asObservable();
	}
	
	refreshPlayer() {
		this.refreshingPlayer = true;
		this.http.get<Player>(`${this.url}player/${this.player_id}/`, this.httpOptions).pipe(
			tap(_ => this.addMessage('info',`fetched player_id=${this.player_id}`)),
			catchError(this.handleError<Player>(`refreshPlayer`))
		).subscribe(player => {
				this.player.next(player);
				this.refreshingPlayer = false;
			});
		this.http.get<PlayerLog[]>(`${this.url}player/${this.player_id}/log/`, this.httpOptions).pipe(
			tap(_ => this.addMessage('info',`fetched playerlogs`)),
			catchError(this.handleError('refreshPlayer', []))
		).subscribe(logs => this.playerLogs.next(logs));
	}
	
	clearPlayer() {
		this.player_id = null;
		this.player.next(null);
		this.playerLogs.next(null);
	}

	upgradePlayer (upgrade: PlayerUpgrade): Observable<any> {
		return this.http.post(`${this.url}player/${this.player_id}/upgrade/`, upgrade, this.httpOptions)
			.pipe(
				tap(_ => {
					this.addMessage('info',`upgraded player_id=${this.player_id} type=${upgrade.upgrade_type} upgrade_id=${upgrade.upgrade_id}`);
					this.refreshPlayer();
				}),
				catchError(this.handleError<any>('upgradePlayer'))
			);
	}
	
	playerAction (player_id: number, playerAction: PlayerAction): Observable<any> {
		return this.http.post(`${this.url}player/${player_id}/${playerAction.action}/`, playerAction, this.httpOptions)
			.pipe(
				tap(result => {
					this.addMessage('success',result['message'],false);
					this.refreshPlayer();
				}),
				catchError(this.handleError<any>('playerAction'))
			);
	}
	
	getBattalion (player_id: number, battalion_number: number): Observable<Battalion> {
		return this.http.get<Battalion>(`${this.url}player/${player_id}/battalion/${battalion_number}/`, this.httpOptions)
			.pipe(
				tap(battalion => this.addMessage('info',`fetched player ${player_id} battalion number ${battalion_number}`)),
				catchError(this.handleError<Battalion>(`getBattalion`))
			);
	}
	
	updateBattalion (player_id: number, battalion_number: number, action: string, update: BattalionUpdate): Observable<any> {
		return this.http.post(`${this.url}player/${player_id}/battalion/${battalion_number}/${action}/`, update, this.httpOptions)
			.pipe(
				tap(_ => {
					this.addMessage('info',`updated action ${action} player ${player_id} battalion number ${battalion_number}`);
					this.refreshPlayer();
				}),
				catchError(this.handleError<any>('updateBattalion'))
			);
	}
	
	getLeaderLevels (): Observable<LeaderLevel[]> {
		return this.http.get<LeaderLevel[]>(`${this.url}leaderlevel/`)
			.pipe(
				tap(leaderlevels => this.addMessage('info',`fetched leaderlevels`)),
				catchError(this.handleError('getLeaderLevels', []))
			);
	}
	
	getGames (): Observable<GamePlayer[]> {
		return this.http.get<GamePlayer[]>(`${this.url}game/`, this.httpOptions)
			.pipe(
				tap(games => this.addMessage('info',`fetched games`)),
				catchError(this.handleError('getGames', []))
			);
	}
	
	getPlayers (game_id: number): Observable<PublicPlayer[]> {
		return this.http.get<PublicPlayer[]>(`${this.url}game/${game_id}/player/`, this.httpOptions)
			.pipe(
				tap(players => this.addMessage('info',`fetched players`)),
				catchError(this.handleError('getPlayers', []))
			);
	}
	
	getTop5 (game_id: number): Observable<PlayerScore[]> {
		return this.http.get<PlayerScore[]>(`${this.url}game/${game_id}/top5/`, this.httpOptions)
			.pipe(
				tap(top5 => this.addMessage('info',`fetched top5`)),
				catchError(this.handleError('getTop5', []))
			);
	}
	
	getStructures (): Observable<Structure[]> {
		return this.http.get<Structure[]>(`${this.url}structure/`)
			.pipe(
				tap(structures => this.addMessage('info',`fetched structures`)),
				catchError(this.handleError('getStructures', []))
			);
	}
	
	getTechnologies (): Observable<Technology[]> {
		return this.http.get<Technology[]>(`${this.url}technology/`)
			.pipe(
				tap(technologies => this.addMessage('info',`fetched technologies`)),
				catchError(this.handleError('getTechnologies', []))
			);
	}
	
	getCreatures (): Observable<Creature[]> {
		return this.http.get<Creature[]>(`${this.url}creature/`)
			.pipe(
				tap(technologies => this.addMessage('info',`fetched creatures`)),
				catchError(this.handleError('getCreatures', []))
			);
	}
	
	getWeaponBases (): Observable<WeaponBase[]> {
		return this.http.get<WeaponBase[]>(`${this.url}weapon_base/`)
			.pipe(
				tap(technologies => this.addMessage('info',`fetched weaponbases`)),
				catchError(this.handleError('getWeaponBases', []))
			);
	}
	
	getWeaponMaterials (): Observable<WeaponMaterial[]> {
		return this.http.get<WeaponMaterial[]>(`${this.url}weapon_material/`)
			.pipe(
				tap(technologies => this.addMessage('info',`fetched weaponmaterials`)),
				catchError(this.handleError('getWeaponMaterials', []))
			);
	}
	
	/**
	* Handle Http operation that failed.
	* Let the app continue.
	* @param operation - name of the operation that failed
	* @param result - optional value to return as the observable result
	*/
	private handleError<T> (operation = 'operation', result?: T) {
		return (error: any): Observable<T> => {

			// TODO: send the error to remote logging infrastructure
			console.error(error); // log to console instead

			// TODO: better job of transforming error for user consumption
			if (error.status == 400 && error.error) {
				this.errors.next({'operation':operation, 'errors':error.error, 'error_keys':Object.keys(error.error)});
			} else if (error.status == 403) {
				
			} else {
				this.addMessage('danger',`${operation} failed: ${error.message}\n${JSON.stringify(error.error)}`,false);
			}

			// Let the app keep running by returning an empty result.
			return of(result as T);
		};
	}
}
