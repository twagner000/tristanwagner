import { BrowserModule } from '@angular/platform-browser';
    import { NgModule } from '@angular/core';
    import { HttpModule } from '@angular/http';

    import { AppComponent } from './app.component';

    @NgModule({
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule ,
        HttpModule //this is the HTTP module
    ],
    providers: [],
    bootstrap: [AppComponent]
    })
    export class AppModule { }