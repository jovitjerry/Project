import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageFaculty } from './manage-faculty';

describe('ManageFaculty', () => {
  let component: ManageFaculty;
  let fixture: ComponentFixture<ManageFaculty>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageFaculty],
    }).compileComponents();

    fixture = TestBed.createComponent(ManageFaculty);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
