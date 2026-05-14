import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AttendanceView } from './attendance-view';

describe('AttendanceView', () => {
  let component: AttendanceView;
  let fixture: ComponentFixture<AttendanceView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AttendanceView],
    }).compileComponents();

    fixture = TestBed.createComponent(AttendanceView);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
