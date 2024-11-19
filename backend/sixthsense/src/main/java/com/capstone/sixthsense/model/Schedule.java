package com.capstone.sixthsense.model;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "schedule")
public class Schedule {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;

	@Column(name = "title")
	private String title;
	
	@Column(columnDefinition = "TEXT", name = "description")
	private String description;

	@Column(name = "dayofweek")
	private int dayofweek;
	
	@Column(name = "time")
	private String time;
	
	@Column(name = "lastRunningDate")
    private LocalDateTime lastRunningDate;
	
	@Column(name = "nextRunningDate")
    private LocalDateTime nextRunningDate;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "project_id", referencedColumnName="id")
    private Project project;
	
	public Schedule() {}
	
    public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public int getDayofweek() {
		return dayofweek;
	}
	public void setDayofweek(int dayofweek) {
		this.dayofweek = dayofweek;
	}
	public String getTime() {
		return time;
	}
	public void setTime(String time) {
		this.time = time;
	}
	public LocalDateTime getLastRunningDate() {
		return lastRunningDate;
	}
	public void setLastRunningDate(LocalDateTime lastRunningDate) {
		this.lastRunningDate = lastRunningDate;
	}
	public LocalDateTime getNextRunningDate() {
		return nextRunningDate;
	}
	public void setNextRunningDate(LocalDateTime nextRunningDate) {
		this.nextRunningDate = nextRunningDate;
	}
	public Project getProject() {
		return project;
	}
	public void setProject(Project project) {
		this.project = project;
	}
	public LocalDateTime calcNexttDateTime() {
		int dayOfWeek = this.dayofweek;
		String time = this.time;

		// 현재 날짜와 시간을 가져옵니다.
        LocalDateTime now = LocalDateTime.now(ZoneId.of("Asia/Seoul"));
        
        // 입력받은 시간을 HH:MM 형식으로 파싱합니다.
        LocalTime targetTime = LocalTime.parse(time);
        
        // 오늘의 요일을 기준으로 입력된 요일의 날짜를 찾습니다.
        LocalDate targetDate = now.toLocalDate();
        int daysToAdd = (dayOfWeek - targetDate.getDayOfWeek().getValue() + 7) % 7;

        if (daysToAdd == 0 && targetTime.isBefore(now.toLocalTime())) {
            // 입력된 요일이 오늘이면서 시간이 이미 지난 경우, 다음 주의 해당 요일로 설정합니다.
            daysToAdd = 7;
        } else if (daysToAdd == 0 && targetTime.isAfter(now.toLocalTime())) {
            // 입력된 요일이 오늘이고 시간이 아직 남은 경우, 날짜를 오늘로 유지합니다.
            daysToAdd = 0;
        } 
        if (daysToAdd > 0) {
            // 입력된 요일이 이번 주 내에 다가오는 경우
            targetDate = targetDate.plusDays(daysToAdd);
        }

        // 계산된 날짜와 시간을 결합하여 LocalDateTime 객체를 반환합니다.
        this.nextRunningDate = LocalDateTime.of(targetDate, targetTime);
        return this.nextRunningDate;
    }
	public boolean isTimeForNextSchedule() {
		return LocalDateTime.now(ZoneId.of("Asia/Seoul")).isAfter(this.nextRunningDate);
	}
	public void updateNextRunningDate() {
		this.calcNexttDateTime();
	}
	public void updateLastRunningDate() {
		this.lastRunningDate = LocalDateTime.now(ZoneId.of("Asia/Seoul"));
	}
}
