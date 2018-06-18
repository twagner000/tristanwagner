import { TestBed, inject } from '@angular/core/testing';

import { CreatureService } from './creature.service';

describe('CreatureService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CreatureService]
    });
  });

  it('should be created', inject([CreatureService], (service: CreatureService) => {
    expect(service).toBeTruthy();
  }));
});
