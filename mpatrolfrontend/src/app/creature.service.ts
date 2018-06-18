import { Injectable } from '@angular/core';
import { Creature } from './creature';
import { CREATURES } from './mock-creatures';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
//import * as _ from 'lodash';



@Injectable({
  providedIn: 'root'
})
export class CreatureService {
	private creaturesUrl = 'http://localhost:8000/mpatrol/api/creature/';

	constructor(
		private http: HttpClient,
		private messageService: MessageService) { }

	getCreatures(): Observable<Creature[]> {
		//this.messageService.add('CreatureService: fetched creatures');
		//return of(CREATURES);
		return this.http
			.get<Creature[]>(this.creaturesUrl)
			.pipe(
				tap(creatures => this.log(`fetched creatures`)),
				catchError(this.handleError('getCreatures', []))
			);
	}
	
	getCreature(pk: number): Observable<Creature> {
		const url = `${this.creaturesUrl}${pk}/`;
		return this.http.get<Creature>(url).pipe(
			tap(_ => this.log(`fetched creature pk=${pk}`)),
			catchError(this.handleError<Creature>(`getCreature pk=${pk}`))
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
		this.messageService.add('CreatureService: ' + message);
	}
}
