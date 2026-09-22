import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { formatDateTime, deserializeDateTime } from "@web/core/l10n/dates";

export class SiteVisitDashboard extends Component {
    static template = "customer_site_visit.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            data: null, loading: false, error: "",
        });
        this.requestId = 0;
        onWillStart(() => this.load());
    }

    async load() {
        const requestId = ++this.requestId;
        this.state.loading = true;
        this.state.error = "";
        try {
            const data = await this.orm.call("customer.site.visit", "get_dashboard_data", []);
            if (requestId === this.requestId) {
                this.state.data = data;
            }
        } catch (error) {
            if (requestId === this.requestId) {
                this.state.error = error.data?.message || _t("Unable to load the dashboard. Please retry.");
            }
        } finally {
            if (requestId === this.requestId) {
                this.state.loading = false;
            }
        }
    }

    pieSlices(rows) {
        const total = rows.reduce((sum, row) => sum + row.count, 0);
        let angle = -Math.PI / 2;
        return rows.map((row, index) => {
            const fraction = total ? row.count / total : 0;
            const end = angle + fraction * 2 * Math.PI;
            const point = (value) => `${100 + 90 * Math.cos(value)},${100 + 90 * Math.sin(value)}`;
            // Two arcs also render a complete circle when only one category has visits.
            const path = fraction ? `M 100,100 L ${point(angle)} A 90,90 0 0,1 ${point((angle + end) / 2)} A 90,90 0 0,1 ${point(end)} Z` : "";
            angle = end;
            return {
                ...row, path,
                color: `hsl(${(index * 137.508 + 260) % 360}, 55%, 48%)`,
                percentage: (fraction * 100).toFixed(1),
            };
        });
    }

    formatDate(value) {
        return value ? formatDateTime(deserializeDateTime(value)) : "";
    }

    openRecords(model, domain, title) {
        return this.action.doAction({
            type: "ir.actions.act_window", name: title, res_model: model,
            views: [[false, "list"], [false, "form"]], domain,
        });
    }

    openVisits(domain) {
        return this.openRecords("customer.site.visit", domain, _t("Site Visits"));
    }

    onSliceKeydown(ev, domain) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            return this.openVisits(domain);
        }
    }

    openFollowups() {
        return this.openRecords("customer.site.visit.finding", this.state.data.finding_domain, _t("Overdue Follow-ups"));
    }

    openVisit(id) {
        return this.action.doAction({
            type: "ir.actions.act_window", res_model: "customer.site.visit",
            res_id: id, views: [[false, "form"]],
        });
    }
}

registry.category("actions").add("customer_site_visit.dashboard", SiteVisitDashboard);
