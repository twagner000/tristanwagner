import { Injectable } from '@angular/core';
import { Player, LeaderLevel, Structure, Technology } from './mpatrol';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

export class PlayerUpgrade {
	constructor(public player_id: number, public upgrade_type: string, public upgrade_id: number) { }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
	providedIn: 'root'
})

export class MpatrolService {
	private url = 'http://localhost:8000/mpatrol/api/';
	private player = new BehaviorSubject<Player>(null);
	
	constructor(
		private http: HttpClient,
		private messageService: MessageService) { }

	getPlayer(): Observable<Player> {
		if (!this.player.getValue()) {
			this.refreshPlayer();
		}
		return this.player.asObservable();
	}
	
	refreshPlayer() {
		this.http.get<Player>(`${this.url}player/11/`).pipe(
			tap(_ => this.log(`fetched player`)),
			catchError(this.handleError<Player>(`refreshPlayer`))
		).subscribe(
			player => this.player.next(player)
		);
	}
	
	clearPlayer() {
		this.player.next(null);
	}

	upgradePlayer (upgrade: PlayerUpgrade): Observable<any> {
		return this.http.post(`${this.url}player/11/upgrade/`, upgrade, httpOptions).pipe(
				tap(_ => {
					this.log(`upgraded player_id=${upgrade.player_id} type=${upgrade.upgrade_type} upgrade_id=${upgrade.upgrade_id}`);
					this.refreshPlayer();
				}),
				catchError(this.handleError<any>('upgradePlayer'))
		);
	}
	
	getLeaderLevels (): Observable<LeaderLevel[]> {
		return this.http.get<LeaderLevel[]>(`${this.url}leaderlevel/`)
			.pipe(
				tap(leaderlevels => this.log(`fetched leaderlevels`)),
				catchError(this.handleError('getLeaderLevels', []))
			);
	}
	
	getStructures (): Observable<Structure[]> {
		return this.http.get<Structure[]>(`${this.url}structure/`)
			.pipe(
				tap(structures => this.log(`fetched structures`)),
				catchError(this.handleError('getStructures', []))
			);
	}
	
	getTechnologies (): Observable<Technology[]> {
		return this.http.get<Technology[]>(`${this.url}technology/`)
			.pipe(
				tap(technologies => this.log(`fetched technologies`)),
				catchError(this.handleError('getTechnologies', []))
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
			this.log(`${operation} failed: ${error.message}`);

			// Let the app keep running by returning an empty result.
			return of(result as T);
		};
	}
	
	private log(message: string) {
		this.messageService.add('MpatrolService: ' + message);
	}
}
