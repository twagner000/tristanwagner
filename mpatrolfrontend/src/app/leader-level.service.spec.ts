import { TestBed, inject } from '@angular/core/testing';

import { LeaderLevelService } from './leader-level.service';

describe('LeaderLevelService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [LeaderLevelService]
    });
  });

  it('should be created', inject([LeaderLevelService], (service: LeaderLevelService) => {
    expect(service).toBeTruthy();
  }));
});
