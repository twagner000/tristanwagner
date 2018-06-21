import { Injectable } from '@angular/core';
import { Technology } from './player';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';
import { HttpClient } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
	providedIn: 'root'
})

export class TechnologyService {
	private url = 'http://localhost:8000/mpatrol/api/technology/';

	
	constructor(
		private http: HttpClient,
		private messageService: MessageService) { }

	getTechnologies (): Observable<Technology[]> {
		return this.http.get<Technology[]>(this.url)
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
		this.messageService.add('TechnologyService: ' + message);
	}
}