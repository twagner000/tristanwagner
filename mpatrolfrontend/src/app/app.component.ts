import { Component } from '@angular/core';
//    import { Http, Response } from '@angular/http';
//    import { Observable } from 'rxjs';
//    import 'rxjs/operators';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
    })
    export class AppComponent {
    title = 'Mossflower Patrol Game';
    url : string = 'http://localhost:8000/mpatrol/api/creature/';


    constructor(){}
	/*constructor(private http : Http){}
	public getCreatures(){

        this.http.get(this.url).toPromise().then((res)=>{
            console.log(res.json());
        });

    }*/
}